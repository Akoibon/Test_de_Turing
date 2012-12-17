#!/usr/bin/env python
# coding=utf-8
import socket, glib, sys
import gtk 
import pygtk
import formating

class Interface:
	def __init__(self,controller):
		self.controller = controller
		self.builder = gtk.Builder()  
		self.builder.add_from_file("joueur_client.view.glade")
		self.window = self.builder.get_object("window1")
		self.entry = self.builder.get_object("entry1")
		self.liststore = self.builder.get_object("liststore1")
		self.robot = self.builder.get_object("robot")
		self.human = self.builder.get_object("human")
		self.send = self.builder.get_object("send")
		self.reload = self.builder.get_object("reload")
		self.scrolledwindow = self.builder.get_object("scrolledwindow1")
		self.builder.connect_signals(self)
		#connect un signal en plus pour gerer le scrolledwindow
		self.scrolledwindow.get_vadjustment().connect("changed", self.changed_cb)


	def on_reload_clicked(self, widget):
		self.entry.set_text("")
		self.liststore.clear()
		self.set_active_button(False,False)
		#++passer la main au controller
		self.controller.reload()	

	def run(self):
		self.window.show_all()

	def on_mainWindow_destroy(self, widget):
		self.controller.sock.close()
		sys.exit(0)
	
	def on_robot_clicked(self, widget):
		self.print_text("info","Vous avez votez pour un robot")
		self.set_active_button(False,False)
		self.controller.vote_robot()

	def on_human_clicked(self, widget):
		self.print_text("info","Vous avez votez pour un humain")
		#++print the result -> win/loose
		#stop the game 	, print a message of result for mysterious. clear mysterious window
		self.set_active_button(False,False)
		self.controller.vote_human()

		
	def changed_cb(self, widget):
		widget.set_value(widget.get_upper())


	def on_send_clicked(self, widget):
		text = self.entry.get_text()
		if text != "":
			self.controller.send_text(text)
			self.print_text("moi",text)
			self.entry.set_text("")	

	def print_text(self,name,text):
		text = formating.from_bot(text)
		self.liststore.append([str(name),str(text)])
		self.scrolledwindow.get_vadjustment().set_value( self.scrolledwindow.get_vadjustment().get_upper())

	def set_active_button(self,val,reload):
		self.robot.set_sensitive(val)
		self.human.set_sensitive(val)
		self.send.set_sensitive(val)
		self.reload.set_sensitive(reload)


	def on_entry1_key_press_event(self, widget, keyboard):
		#seulement la touche entre permet d envoyer un message
		if (65293 == keyboard.keyval) & (self.send.get_sensitive()):
			self.on_send_clicked(False)
			

class Controller:
	def __init__(self,sock):
		self.view = Interface(self)
		self.sock = sock
		

	def run(self):
		self.view.run()
		self.reload()

		
	def reload(self):
		# envoyer un message a mysterious pour lui dire de clear son interface
		self.view.set_active_button(False,False)
		self.print_text("info","Le jeu va bientot commencer")
		self.sock.send("++++reload++++")


	def print_text(self,name,text):
		self.view.print_text(name,text)	

	
	def send_text(self,text):
		try:	
			self.sock.send(text)

		except socket.error, detail:
			print "socket.error", detail

	def vote_robot(self):
		self.sock.send("++++vote=robot++++")

	def vote_human(self):
		self.sock.send("++++vote=human++++")

def handle_read_sock (source, condition):
	msg = source.read()	
	if not msg:
		print "EOF from socket"
		sys.exit(0)
		
	#++++RELOAD_OK++++
	if msg == "++++reload_ok++++":
		control.view.liststore.clear()
		control.print_text("info","Le Test de Turing commence !")
		control.print_text("info","Tu dois deviner si hide est un humain ou un robot !")
		control.print_text("info","C'est toi qui dois parler en premier")
		control.view.set_active_button(True,True)
	
	elif msg == "++++robot=win++++":
		control.print_text("info","Tu gagnes ! Le robot ne se fait pas passer pour un humain")
		control.print_text("info", "Pour recommencer une nouvelle partie, il faut cliquer sur le bouton en haut à droite :)")
		control.view.set_active_button(False,True)
	elif msg == "++++robot=loose++++":
		control.print_text("info","Tu perds ! Ce n'est pas un robot mais un humain")
		control.print_text("info", "Pour recommencer une nouvelle partie, il faut cliquer sur le bouton en haut à droite :)")
		control.view.set_active_button(False,True)
	elif msg == "++++human=loose++++":
		control.print_text("info","Tu perds ! Le robot se fait passer pour un humain")
		control.print_text("info", "Pour recommencer une nouvelle partie, il faut cliquer sur le bouton en haut à droite :)")
		control.view.set_active_button(False,True)
	elif msg == "++++human=win++++":
		control.print_text("info","Tu gagnes ! Tu as reconnu un humain")
		control.print_text("info", "Pour recommencer une nouvelle partie, il faut cliquer sur le bouton en haut à droite :)")
		control.view.set_active_button(False,True)
	else:
		control.print_text("hide",msg)
	return True

if __name__ == "__main__":
	if 3 != len(sys.argv):
		print "+++Turing_test_HELP+++"
		print "\tjoueur_client.py HOST PORT"
		print "You can also go to the README.fr"
		print ""


	else:
		#creation de la socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#connection de la socket
		sock.connect ((str(sys.argv[1]), int(sys.argv[2])))
		
		#creation de la superbe interface graphique pour le joueur
		control = Controller(sock)
		control.run()
		
		#gestion du multiprocessus: socket + gtk
		channel_sock = glib.IOChannel (sock.fileno())
		channel_sock.set_flags (channel_sock.get_flags() | glib.IO_FLAG_NONBLOCK)
		channel_sock.add_watch (condition=glib.IO_IN, callback=handle_read_sock)
		
		#on envoie la sauce avec la boucle principale
		glib.MainLoop().run()
