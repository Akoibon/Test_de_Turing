# coding=utf-8
import socket, sys, glib
import gtk 
import pygtk
import cleverbot
import statistique
import time
import random
import formating

class Interface_hideman():
	def __init__(self,controller):
		#extrait les elements du glade
		self.builder = gtk.Builder()  
		self.builder.add_from_file("server_hideman.view.glade")
		self.window = self.builder.get_object("window1")
		self.entry = self.builder.get_object("entry1")
		self.labelhost = self.builder.get_object("host")
		self.labelport = self.builder.get_object("port")
		self.liststore = self.builder.get_object("liststore1")
		self.spinbutton = self.builder.get_object("spinbutton1")
		self.robot = self.builder.get_object("robot")
		self.human = self.builder.get_object("human")
		self.send = self.builder.get_object("send")
		self.auto_accept_robot = self.builder.get_object("auto_accept_robot")
		self.scrolledwindow = self.builder.get_object("scrolledwindow1")
		self.builder.connect_signals(self)
		#initialise le controller
		self.controller = controller
		#initialise le label
		self.labelhost.set_text(str(controller.address[0]))
		self.labelport.set_text(str(controller.address[1]))
		#connect un signal en plus pour gerer le scrolledwindow
		self.scrolledwindow.get_vadjustment().connect("changed", self.changed_cb)

	def run(self):
		self.window.show_all()

	def on_mainWindow_destroy(self, widget):
		self.controller.socket.close()
		sock_serv.close()
		sys.exit(0)
	
	def on_send_clicked(self, widget):
		text = self.entry.get_text()
		if text != "":
			self.controller.send_text(text)
			self.print_text("Moi",text)
			self.entry.set_text("")		

	def changed_cb(self, widget):
		widget.set_value(widget.get_upper())


	def print_text(self,name,text):
		text = formating.from_bot(text)
		self.liststore.append([str(name),str(text)])

	def on_human_clicked(self, widget):
		self.set_active_button(False,True)
		global bot
		bot=False
		self.on_clear()
		self.print_text("info","Le test commence, c'est toi qui joue")
		self.controller.socket.send("++++reload_ok++++")		
	
	def on_robot_clicked(self, widget):
		self.set_active_button(False,False)
		self.controller.cb=cleverbot.Session()
		global bot
		bot=True
		self.on_clear()
		self.print_text("info","Le test commence, c'est le robot qui joue")
		self.controller.socket.send("++++reload_ok++++")
		
	def on_clear(self):
		self.entry.set_text("")
		self.liststore.clear()

	def set_active_button(self,human_robot,send):
		self.robot.set_sensitive(human_robot)
		self.human.set_sensitive(human_robot)
		self.send.set_sensitive(send)

	
	def on_entry1_key_press_event(self, widget, keyboard):
		#seulement la touche entre permet d envoyer un message
		if (65293 == keyboard.keyval) & (self.send.get_sensitive()):
			self.on_send_clicked(False)

	
class TrControllerClient():
	def __init__(self,socket ,address):
		self.address = address		
		self.view = Interface_hideman(self)
		self.socket = socket
		
		
	def send_text(self,text):
		try:	
			self.socket.send(text)

		except socket.error, detail:
			print "socket.error", detail

	def print_text(self,name,text):
		self.view.print_text(name,text)
	
	def run(self):
		self.view.run()
		#useless
		self.view.set_active_button(False,False)
		
	def reload(self):
		self.view.on_clear()
		self.new_games()

	def new_games(self):
		#+++hideman choisi son role+++
		if self.view.auto_accept_robot.get_active():
			self.view.print_text("info","auto accept ok")
			self.view.on_robot_clicked(False)
		else:	
			self.view.print_text("info","Debut d'une nouvelle partie")
			self.view.print_text("info","Tu dois choisir ton role")
			self.view.set_active_button(True,False)
				
			
def handle_read_sock (source, condition):
	msg = source.read()
	#++++Test_de_fin_de_connexion++++
	if not msg:
		print "EOF from socket"
		sys.exit(0)
	
	#RECEPTION
	
	if msg == "++++reload++++":
		tr.reload()
		if do_stat:
			stat.load()
			stat.add_partie()
			stat.save()
	elif msg == "++++vote=robot++++":
		tr.view.set_active_button(False,False)
		if do_stat:
			stat.load()
			stat.vote(True,bot)
			stat.save()
		tr.print_text("info","La partie se termine")
		if(bot):
			tr.print_text("info","Le robot se fait demasquer")
			sock.send("++++robot=win++++")
		else:
			tr.print_text("info","Now you can say : I fail the turing test")
			sock.send("++++robot=loose++++")
	elif msg == "++++vote=human++++":
		tr.view.set_active_button(False,False)
		if do_stat:
			stat.load()
			stat.vote(False,bot)
			stat.save()
		tr.print_text("info","La partie se termine")
		if(bot):
			tr.print_text("info","Le robot se fait passer pour un humain")
			sock.send("++++human=loose++++")
		else:
			tr.print_text("info","Le joueur a reconnu que tu es un humain")
			sock.send("++++human=win++++")
	elif bot:
		tr.print_text("joueur",msg)
		databot=tr.cb.Ask(msg)
		time.sleep(random.randint(3,5))
		sock.send(databot)
		tr.print_text("bot",databot)

	else:
		#++++PRINT_text++++
		tr.print_text("joueur",msg)

		
	return True

#main principal
if __name__ == "__main__":
	if 3 != len(sys.argv)  | len(sys.argv) != 4:
		print "+++Turing_test_HELP+++"
		print "\tserver_hideman.py HOST PORT"
		print "\tserver_hideman.py HOST PORT [STAT]"
		print "You can also go to the README.fr"
		print ""
	else:
		#statistique pour le jeu
		if len(sys.argv)==4:
			stat = statistique.Stat(str(sys.argv[3]))
			print "Statistique des parties dans le fichier:{0}".format(sys.argv[3])
			do_stat=True
		
		else:
			do_stat=False		
		
		#creation de la socket
		sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock_serv.bind((str(sys.argv[1]), int(sys.argv[2])))
		sock_serv.listen(1)

		print "En attente de joueur sur HOST:{0} PORT:{1}".format(sys.argv[1],sys.argv[2])

		#en attente d'un joueur
		(sock, address) = sock_serv.accept()

		#affichage de la magnifique interface graphique
		global bot
		tr = TrControllerClient(sock,address)
		tr.run()

		#gestion du multiprocessus: socket + gtk
		channel_sock = glib.IOChannel (sock.fileno())
		channel_sock.set_flags (channel_sock.get_flags() | glib.IO_FLAG_NONBLOCK)
		channel_sock.add_watch (condition=glib.IO_IN, callback=handle_read_sock)

		#on envoie la sauce avec la boucle principale
		glib.MainLoop().run()
