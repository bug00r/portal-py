import subprocess

subprocess.call(["python","-m","unittest", "discover", "-s",".","--pattern",'*_test.py'])