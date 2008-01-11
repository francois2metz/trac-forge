from mod_python import apache
from trac.env import open_environment
from dircache import listdir
from jinja import Template, Context, FileSystemLoader
import time
from os import path

class Config:
	"Contient la configuration"
	trac_href = "/"
	trac_dir = "/home/etna/trac"
	demo_href = "/demo"
	demo_dir = "/home/etna/www/demo"
	archives_href = "/archives"
	archives_dir = "/home/etna/www/archives"
	template_dir = "/home/etna/www/templates"

class TracProject:
	"Instance d'un projet trac"
	def __init__(self, path):
		self.path = path
		self.env = open_environment(path)
	def get_env(self):
		return self.env
	def get_repos(self):
		return self.env.get_repository()

class TracProjects:
	"Tous les projets trac"
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
	"traitement de la requete"
	config = Config()
	if req.uri == "/admin":
		view_admin(req, config)
	elif req.uri == "/a" or req.uri == "/z" or req.uri == "/":
		view_index(req, config)
	else:
		view_404(req, config)
	return apache.OK

def view_admin(req, config):
	req.content_type = 'text/html'
	t = Template('admin', FileSystemLoader(config.template_dir))
	c = Context({
		'users' : [{'name' : 'toto'}]
	})
	req.write(t.render(c))

def view_404(req, config):
	"Page d'erreur 404"
	req.content_type = 'text/html'
	req.status = 404
	t = Template('404', FileSystemLoader(config.template_dir))
	c = Context({})
	req.write(t.render(c))

def view_index(req, config):
	"Index des projets"
	req.content_type = 'text/html'
	now = time.time()
	tracProjects = TracProjects(config.trac_dir)
	projects = []
	for project in tracProjects:
		try:
			env = project.get_env()
			repos = project.get_repos()
			#  
			lastChange = repos.get_changeset(repos.youngest_rev)
			dateDiff = now - lastChange.date
			nbYears = dateDiff / (60 * 60 * 24 * 30 * 12)
			# TODO: Generique
			if nbYears > 1:
				messageDiff = " plus de " + str(int(bYears)) + " an"
			else:
				nbMonths = dateDiff / (60 * 60 * 24 * 30)
				if nbMonths > 1:
					messageDiff = str(int(nbMonths)) + " mois"
				else:
					nbDays = dateDiff / (60 * 60 * 24)
					if nbDays > 1:
						messageDiff = str(int(nbDays)) + " jours "
					else:
						nbHours = dateDiff / (60 * 60)
						if nbHours > 1:
							messageDiff = "plus de " + str(int(nbHours)) + " heures"
						else:
							messageDiff = "moins d'une heure"
			dir = path.basename(project.path)
			# DEMO
			demo = False
			if path.exists("%s/%s" % (config.demo_dir, dir)):
				demo = True
			# TARBALL
			tarball = False
			if path.exists("%s/%s" % (config.archives_dir, dir)):
				tarball = True
			proj = {'name' : env.project_name,
				'href' : config.trac_href + dir,
				'description' : env.project_description,
				'activity' : {
					'lastrev' : repos.youngest_rev,
					'lastauthor' : lastChange.author,
					'lastdate' : messageDiff,
					'lastmessage' : lastChange.message,
					'datediff' : dateDiff
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
		except Exception, e:
			pass
	if req.uri == "/a":
		projects.sort(lambda x,y: cmp(x['name'], y['name']))
		sort = "a"
	elif req.uri == "/z":
		projects.sort(lambda x,y: cmp(y['name'], x['name']))
		sort = "z"
	else:
		projects.sort(lambda x, y: cmp(x['activity']['datediff'], y['activity']['datediff']))
		sort = "b"
	t = Template('projects', FileSystemLoader(config.template_dir))
	c = Context({
		'projects' : projects,
		'sort' : sort
	})
	req.write(t.render(c))


