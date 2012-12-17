# coding=utf-8
import re

def from_bot(st):
		st = st.strip()
		m = re.search(r'[\?\.\!]$',st)
		if m is None:
			st += '.'
		st = st.replace("&eacute;","é")
		st = st.replace("&ntilde","n") #??
		st = st.replace("&ccedil;","ç")
		st = st.replace("&egrave;","è")
		st = st.replace("&agrave;","à")
		st = st.replace("&ecirc;","ê")
		st = st.replace("&ocirc;","ô")
		st = st.replace("&quest;","q")
		st = '{0}{1}'.format(st[0].upper(), st[1:])
		return st
