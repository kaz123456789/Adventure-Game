import sys
import subprocess
# p = subprocess.getoutput("{} ./adventure.py < solution.txt".format(sys.executable))
# print(p)
# p1 = subprocess.getoutput("{} ./adventure.py < gameover.txt".format(sys.executable))
# print(p1)
p2 = subprocess.getoutput("{} ./adventure.py < gameplay1.txt".format(sys.executable))
print(p2)
