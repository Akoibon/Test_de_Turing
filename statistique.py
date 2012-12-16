import cPickle
import os

#parametre: voteRobotWin = le joueur vote pour un robot et le joueur gagne
#-> robot demasquer

#parametre: voteRobotLoose = le joueur vote pour un robot et le joueur perd
#-> hideman fail the turing test

#parametre: voteHumanWin = le joueur vote pour un human et le joueur gagne
#-> hideman est reconnu comme humain

#parametre: voteHumanLoose = le joueur vote pour un humain et le joueur perd
#-> robot se fait passer pour un humain 

class Stat:
	def __init__(self,fichier):
		self.fichier = fichier
		if os.path.exists(fichier):
			self.load()
		else :
			self.init()
			#creer
			self.save()
				
	def save(self):
		sauvegarde = [self.nbPartie , self.voteRobotWin , self.voteRobotLoose , self.voteHumanWin, self.voteHumanLoose ]
		monFichier=open(str(self.fichier),'w')
		
		cPickle.dump(sauvegarde,monFichier)
		monFichier.close()
		
	def load(self):
		monFichier=open(str(self.fichier),'r')
		sauvegarde=cPickle.load(monFichier )
		self.set(sauvegarde[0],sauvegarde[1],sauvegarde[2],sauvegarde[3],sauvegarde[4])

	def init(self):
		self.set(0,0,0,0,0)
		
	def print_stat(self):
		print "nbPartie : %s"%(self.nbPartie)
		print "voteRobotWin : %s"%(self.voteRobotWin)
		print "voteRobotLoose : %s"%(self.voteRobotLoose)
		print "voteHumanWin : %s"%(self.voteHumanWin)
		print "voteHumanLoose : %s"%(self.voteHumanLoose)

	def set(self,nbPartie,voteRobotWin,voteRobotLoose,voteHumanWin,voteHumanLoose):
		self.nbPartie = nbPartie
		self.voteRobotWin = voteRobotWin
		self.voteRobotLoose = voteRobotLoose
		self.voteHumanWin = voteHumanWin
		self.voteHumanLoose = voteHumanLoose

	#[vote -> robot=True,human=false]
	def vote(self,vote,robot):
		if(robot):
			if(vote):
				self.voteRobotWin = self.voteRobotWin+1
			else:
				self.voteRobotLoose = self.voteRobotLoose+1
		else:
			if(vote):
				self.voteHumanWin = self.voteHumanWin+1
			else:
				self.voteHumanLoose = self.voteHumanLoose+1

	def add_partie(self):
		self.nbPartie = self.nbPartie+1

	def help(self):
		print "save"
		print "load"
		print "init"
		print "print_stat"
		print "vote [=vote] [=bot]"
