import re
import sys
#https://github.com/aristofor/aristuff/blob/master/ari/utils/base36.py
#http://www.virtualenv.org/en/latest/
#python formating.py 'KtytPyp!'
st = sys.argv[1].strip()
print st
m = re.search(r'[\?\.\!]$',st)

if m is None:
	st += '.'

print repr(st)


st = '{0}{1}'.format(st[0].upper(), st[1:])

print st

raise SystemExit()

#.title()
#.capitalize()



#.replace("old","new")
#&eacute;
