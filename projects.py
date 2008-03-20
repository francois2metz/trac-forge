from mod_python import apache
from trac.env import open_environment
from dircache import listdir
from jinja import Environment, FileSystemLoader
import time
from os import path

class Config:
	"""Contient la configuration"""
	root_dir = "/var/www/tracforge"
	forge_href = "/tracforge"
	forge_dir = root_dir+"/tracforge"
	template_dir = forge_dir+"/templates"
	media_href = "/media/"
	trac_href = "/trac/"
	trac_dir = root_dir+"/trac"
	demo_href = "/demo"
	demo_dir = root_dir+"/demo"
	archives_href = "/archive"
	archives_dir = root_dir+"/archive"

class TracProject:
	""""Instance d'un projet trac"""
	def __init__(self, path):
		self.path = path
		self.env = open_environment(path)
	def get_env(self):
		return self.env
	def get_repos(self):
		return self.env.get_repository()

class TracProjects:
	""""Tous les projets trac"""
	def __init__(self, trac_dir):
		self.trac_dir = trac_dir
		self._projects = self._get_projects()
		self.index = 0
	def next(self):
		nb = len(self._projects)
		if self.index < nb:
			project = self._projects[self.index]
			self.index = self.index + 1
			return project
		else:
			raise StopIteration
	def __iter__(self):
		self.index = 0
		return self
	def _get_projects(self):
		projects = listdir(self.trac_dir)
		tracprojects = []
		for project in projects:
			tracprojects.append(TracProject("%s/%s" % (self.trac_dir, project)))
		return tracprojects

def handler(req):
	"""traitement de la requete"""
	config = Config()
	if req.uri == config.forge_href+"/admin":
		view_admin(req, config)
	elif req.uri == config.forge_href+"/a" or req.uri == config.forge_href+"/z" or req.uri == config.forge_href+"/":
		view_index(req, config)
	else:
		view_404(req, config)
	return apache.OK

def view_admin(req, config):
	req.content_type = 'text/html'
	env = Environment(loader=FileSystemLoader(config.template_dir))
	tmpl = env.get_template("admin.html")
	context = {
		'users' : [{'name' : 'toto'}],
		'forge_href' : config.forge_href,
		'media_href' : config.media_href
	}
	req.write(tmpl.render(context))

def view_404(req, config):
	"""Page d'erreur 404"""
	req.content_type = 'text/html'
	req.status = 404
	env = Environment(loader=FileSystemLoader(config.template_dir))
	tmpl = env.get_template("404.html")
	context = {
		'forge_href' : config.forge_href
	}
	req.write(tmpl.render(context))


def repository_diff_message(lastChange):
	project_date_diff = time.time() - lastChange.date
	nbYears = project_date_diff / (60 * 60 * 24 * 30 * 12)
	if nbYears > 1:
		project_message_diff = " plus de " + str(int(nbYears)) + " an"
	else:
		nbMonths = project_date_diff / (60 * 60 * 24 * 30)
		if nbMonths > 1:
			project_message_diff = str(int(nbMonths)) + " mois"
		else:
			nbDays = project_date_diff / (60 * 60 * 24)
			if nbDays > 1:
				project_message_diff = str(int(nbDays)) + " jours "
			else:
				nbHours = project_date_diff / (60 * 60)
				if nbHours > 1:
					project_message_diff = "plus de " + str(int(nbHours)) + " heures"
				else:
					project_message_diff = "moins d'une heure"
	return project_message_diff


def view_index(req, config):
	"""Index des projets"""
	req.content_type = 'text/html'
	tracProjects = TracProjects(config.trac_dir)
	projects = []
	for project in tracProjects:
		# Prepare variable to set project
		env = project.get_env()
		repos = project.get_repos()
		dir = path.basename(project.path)
		try:
			lastChange = repos.get_changeset(repos.youngest_rev)
			project_name = env.project_name
			project_href = config.trac_href + dir
			project_description = env.project_description
			project_youngest_rev = repos.youngest_rev
			project_last_author = lastChange.author
			project_last_message = lastChange.message
			project_laste_date = lastChange.date
			project_date_diff = time.time() - lastChange.date
			project_message_diff = repository_diff_message(lastChange)
		# in the case of the repository has not yet been modified
		except:
			project_last_author = ""
			project_last_message = "This repository has not yet been modified"
			project_laste_date = time.time()
			project_name = env.project_name
			project_href = config.trac_href + dir
			project_description = env.project_description
			project_youngest_rev = "0"
			project_date_diff = time.time() - time.time()
			project_message_diff = "0 minutes"
		# DEMO
		demo = False
		if path.exists("%s/%s" % (config.demo_dir, dir)):
			demo = True
		# TARBALL
		tarball = False
		if path.exists("%s/%s" % (config.archives_dir, dir)):
			tarball = True
		# a project
		proj = {'name' : project_name,
			'href' : project_href,
			'description' : project_description,
			'activity' : {
				'lastrev' : project_youngest_rev,
				'lastauthor' : project_last_author,
				'lastdate' : project_message_diff,
				'lastmessage' : project_last_message,
				'datediff' : project_date_diff
			},
			'demo' : {
				'enable' : demo,
				'href' : "%s/%s" % (config.demo_href, dir)
			},
			'tarball' : {
				'enable' : tarball,
				'href' : "%s/%s" % (config.archives_href, dir)
			}
		}
		projects.append(proj)
	# sort projects
	if req.uri == config.forge_href+"/a":
		projects.sort(lambda x,y: cmp(x['name'], y['name']))
		sort = "a"
	elif req.uri == config.forge_href+"/z":
		projects.sort(lambda x,y: cmp(y['name'], x['name']))
		sort = "z"
	else:
		projects.sort(lambda x, y: cmp(x['activity']['datediff'], y['activity']['datediff']))
		sort = "b"
	# apply template
	environment = Environment(loader=FileSystemLoader(config.template_dir))
	template = environment.get_template("projects.html")
	context = {
		'projects' : projects,
		'sort' : sort,
		'forge_href' : config.forge_href,
		'media_href' : config.media_href,
		'debug' : req.uri
	}
	req.write(template.render(context))


