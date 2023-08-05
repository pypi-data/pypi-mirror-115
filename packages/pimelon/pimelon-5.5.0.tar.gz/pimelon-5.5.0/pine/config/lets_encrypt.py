# imports - standard imports
import os

# imports - third party imports
import click

# imports - module imports
import pine
from pine.config.common_site_config import get_config
from pine.config.nginx import make_nginx_conf
from pine.config.production_setup import service
from pine.config.site_config import get_domains, remove_domain, update_site_config
from pine.utils import CommandFailedError, exec_cmd, update_common_site_config


def setup_letsencrypt(site, custom_domain, pine_path, interactive):

	site_path = os.path.join(pine_path, "sites", site, "site_config.json")
	if not os.path.exists(os.path.dirname(site_path)):
		print("No site named "+site)
		return

	if custom_domain:
		domains = get_domains(site, pine_path)
		for d in domains:
			if (isinstance(d, dict) and d['domain']==custom_domain):
				print(f"SSL for Domain {custom_domain} already exists")
				return

		if not custom_domain in domains:
			print(f"No custom domain named {custom_domain} set for site")
			return

	if interactive:
		click.confirm('Running this will stop the nginx service temporarily causing your sites to go offline\n'
			'Do you want to continue?',
			abort=True)

	if not get_config(pine_path).get("dns_multitenant"):
		print("You cannot setup SSL without DNS Multitenancy")
		return

	create_config(site, custom_domain)
	run_certbot_and_setup_ssl(site, custom_domain, pine_path, interactive)
	setup_crontab()


def create_config(site, custom_domain):
	config = pine.config.env().get_template('letsencrypt.cfg').render(domain=custom_domain or site)
	config_path = f'/etc/letsencrypt/configs/{custom_domain or site}.cfg'
	create_dir_if_missing(config_path)

	with open(config_path, 'w') as f:
		f.write(config)


def run_certbot_and_setup_ssl(site, custom_domain, pine_path, interactive=True):
	service('nginx', 'stop')
	get_certbot()

	try:
		interactive = '' if interactive else '-n'
		exec_cmd(f"{get_certbot_path()} {interactive} --config /etc/letsencrypt/configs/{custom_domain or site}.cfg certonly")
	except CommandFailedError:
		service('nginx', 'start')
		print("There was a problem trying to setup SSL for your site")
		return

	ssl_path = f"/etc/letsencrypt/live/{custom_domain or site}/"
	ssl_config = { "ssl_certificate": os.path.join(ssl_path, "fullchain.pem"),
					"ssl_certificate_key": os.path.join(ssl_path, "privkey.pem") }

	if custom_domain:
		remove_domain(site, custom_domain, pine_path)
		domains = get_domains(site, pine_path)
		ssl_config['domain'] = custom_domain
		domains.append(ssl_config)
		update_site_config(site, { "domains": domains }, pine_path=pine_path)
	else:
		update_site_config(site, ssl_config, pine_path=pine_path)

	make_nginx_conf(pine_path)
	service('nginx', 'start')


def setup_crontab():
	from crontab import CronTab

	job_command = '/opt/certbot-auto renew -a nginx --post-hook "systemctl reload nginx"'
	job_comment = 'Renew lets-encrypt every month'
	print(f"Setting Up cron job to {job_comment}")

	system_crontab = CronTab(user='root')

	for job in system_crontab.find_comment(comment=job_comment): # Removes older entries
		system_crontab.remove(job)

	job = system_crontab.new(command=job_command, comment=job_comment)
	job.setall('0 0 */1 * *') # Run at 00:00 every day-of-month
	system_crontab.write()


def create_dir_if_missing(path):
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))


def get_certbot():
	from urllib.request import urlretrieve

	certbot_path = get_certbot_path()
	create_dir_if_missing(certbot_path)

	if not os.path.isfile(certbot_path):
		urlretrieve("https://dl.eff.org/certbot-auto", certbot_path)
		os.chmod(certbot_path, 0o744)


def get_certbot_path():
	return "/opt/certbot-auto"


def renew_certs():
	# Needs to be run with sudo
	click.confirm('Running this will stop the nginx service temporarily causing your sites to go offline\n'
		'Do you want to continue?',
		abort=True)

	setup_crontab()

	service('nginx', 'stop')
	exec_cmd(f"{get_certbot_path()} renew")
	service('nginx', 'start')


def setup_wildcard_ssl(domain, email, pine_path, exclude_base_domain):

	def _get_domains(domain):
		domain_list = [domain]

		if not domain.startswith('*.'):
			# add wildcard caracter to domain if missing
			domain_list.append(f'*.{domain}')
		else:
			# include base domain based on flag
			domain_list.append(domain.replace('*.', ''))

		if exclude_base_domain:
			domain_list.remove(domain.replace('*.', ''))

		return domain_list

	if not get_config(pine_path).get("dns_multitenant"):
		print("You cannot setup SSL without DNS Multitenancy")
		return

	get_certbot()
	domain_list = _get_domains(domain.strip())

	email_param = ''
	if email:
		email_param = f'--email {email}'

	try:
		exec_cmd(f"{get_certbot_path()} certonly --manual --preferred-challenges=dns {email_param} \
			--server https://acme-v02.api.letsencrypt.org/directory \
			--agree-tos -d {' -d '.join(domain_list)}")

	except CommandFailedError:
		print("There was a problem trying to setup SSL")
		return

	ssl_path = f"/etc/letsencrypt/live/{domain}/"
	ssl_config = {
		"wildcard": {
			"domain": domain,
			"ssl_certificate": os.path.join(ssl_path, "fullchain.pem"),
			"ssl_certificate_key": os.path.join(ssl_path, "privkey.pem")
		}
	}

	update_common_site_config(ssl_config)
	setup_crontab()

	make_nginx_conf(pine_path)
	print("Restrting Nginx service")
	service('nginx', 'restart')
