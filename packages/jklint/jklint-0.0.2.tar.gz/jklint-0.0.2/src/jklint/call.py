from subprocess import run,DEVNULL
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

def lint():
    command = "java"
    option1 = "-jar"
    filename = 'jenkins-cli.jar'
    option2 = "-s"
    url = config['url']
    protocol = "-webSocket"
    option3 = "-auth"
    username = config['username']
    option4 = "declarative-linter"
    jenkins_path = config['jenkins_path']
    args=[]
    args.append(command)
    args.append(option1)
    args.append(filename)
    args.append(option2)
    args.append(url)
    args.append(protocol)
    args.append(option3)
    args.append(username)
    args.append(option4)
    f = open(str(jenkins_path), "r")
    return str(run(args, encoding='UTF-8',input=f.read(),capture_output=True, text=True)).replace(str(url),'jenkins-url').replace(str(username),'user')