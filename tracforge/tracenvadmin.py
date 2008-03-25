#!/usr/bin/python
#
# trac-admin initenv <projectname> <db> <repostype> <repospath> <templatepath>
#
import os
import time

class Tracenvadmin:

	def __init__(self):
		self.db = "sqlite:db/trac.db"
		self.template = "/usr/share/trac/templates"
		self.rootpath = "/home/francois/dev"
		self.tracpath = self.rootpath+"/trac/"
		self.svnpath = self.rootpath+"/svn/"
		self.svn = "svn"
	
	def createenv(self,projectname = None):
		os.chdir(self.svnpath)
		os.system("/usr/bin/svnadmin create "+projectname)
		os.chdir(self.tracpath)	
		os.system("/usr/bin/trac-admin "+projectname+" initenv "+projectname+" "+self.db+" "+self.svn+" "+self.svnpath+projectname+" "+self.template)


if __name__ == "__main__":
	env = Tracenvadmin()
	env.createenv("test")

