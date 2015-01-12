from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

# You'll want to update the REPO_URL variable with the URL 
# your own Git repo on its code sharing site
REPO_URL = 'https://github.com/Andyccs/TDDpython.git'

def deploy():
	# env.host will contain the address of the server we've 
	# specified at the command line, eg: www.andyccs.com
	# env.user will contain the username you're using to log
	# in to the server.
	site_folder = '/home/%s/sites/%s' % (env.user, env.host)
	source_folder = site_folder + '/source'

	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database','static','virtualenv','source'):
		# run is the most common Fabric command. It says "run this
		# shell command on the server".
		# mkdir -p is a useful flavor of mkdir, which is better in 
		# two ways: it can create directories several levels deep, 
		# and it only creates them if necessary. 
		run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
	# exists checks whether a directory or file already exists on
	# the server. We look for the .git hidden folder to check 
	# whether the repo has already been cloned in that folder
	if exists(source_folder + '/.git'):
		# Many commands start with a cd in order to set the current
		# working directory. Fabric doesn't have any state, so it 
		# doesn't remember what directory you're in from one run to 
		# the next
		# git fetch inside an existing repository pulls down all the
		# latest commits from the Web.
		run('cd %s && git fetch' % (source_folder,))
	else:
		# Alternatively we use git clone with the repo URL to bring
		# down a fresh source tree
		run('git clone %s %s' % (REPO_URL,source_folder))
	# Fabric local command runs a command on your local machine. 
	# Here we capture the output from that git log invocation to get
	# the hash of the current commit that's in your local tree. That 
	# means the server will end up with whatever code is currently 
	# checked out on your machine (as long as you've pushed it up to 
	# the server)
	current_commit = local('git log -n 1 --format=%H', capture=True)
	# We reset --hard to that commit, which will blow away current 
	# changes in the server's code directory.
	run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	# The Fabric sed command does a string substitution in a file; 
	# here it's changing DEBUG from True to False
	sed(settings_path, "DEBUG = True", "DEBUG = False")
	# And here it is adjusting ALLOWED_HOSTS, using a regex to match
	# the right line
	sed(settings_path,
		'ALLOWED_HOSTS = .+$',
		'ALLOWED_HOSTS = ["%s"]' % (site_name,)
	)
	secret_key_file = source_folder + '/superlists/secret_key.py'
	# Django uses SECRETE_KEY for some of its crypto -- cookies and 
	# CSRF protection. It's good practice to make sure the secret key 
	# on the server is different from the one in your (possibly public)
	# source code repo. This code will generate a new key to import into
	# setting, if there isn't one there already (once your have a secret
	# key, it should stay the same between deploys)
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, "SECRET_KEY = '%s'" % (key,))

	# append just adds a line to the send of a file
	# We are using a relative import to be absolutely sure we're importing 
	# the local module, rather than one from somewhere else on sys.path
	append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	# We look inside virtualenv folder for the pip executable as a way 
	# of checking whether it already exists
	if not exists(virtualenv_folder + '/bin/pip'):
		run('virtualenv --python=python3 %s' % (virtualenv_folder,))
	run('%s/bin/pip install -r %s/requirements.txt' % (
		virtualenv_folder, source_folder
	))

def _update_static_files(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
		source_folder, 
	))

def _update_database(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
		source_folder,
	))
