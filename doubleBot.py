import cleverbot
import time

cb1=cleverbot.Session()
cb2=cleverbot.Session()

r1 = cb1.Ask("Salut")
print "cb1 : Salut" 

while True:
	r2 = cb2.Ask(r1)
	print "cb2 : {0}".format(r2)
        time.sleep(1)
	r1 = cb1.Ask(r2)
        print "cb1 : {0}".format(r1)
	time.sleep(1)

