# coding=utf-8
#not the final version
import cleverbot
import formating

cb1=cleverbot.Session()
cb2=cleverbot.Session()

r1 = cb1.Ask("Salut")
print "cb1 : Salut" 

while True:
	r2 = formating.from_bot(cb2.Ask(formating.to_bot(r1)))
	print "cb2 : {0}".format(r2)
	r1 = formating.from_bot(cb1.Ask(formating.to_bot(r2)))
        print "cb1 : {0}".format(r1)

