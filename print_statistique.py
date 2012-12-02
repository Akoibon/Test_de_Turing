import statistique
import sys

file = str(sys.argv[1])
stat = statistique.Stat(file)
stat.load()
stat.print_stat()
