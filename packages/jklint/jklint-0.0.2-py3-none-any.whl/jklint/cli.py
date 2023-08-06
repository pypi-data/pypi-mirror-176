from argparse import ArgumentParser
import os.path
from os import name
import subprocess
from requests import get
from dotenv import dotenv_values

config = dotenv_values(".env")

def create_parser():
    parser =ArgumentParser(description="""
    Configuration to Validate Jenkinsfile sent to the Jenkins Client
    """)
    parser.add_argument('config',default=None)
    parser.add_argument('go',default=None,nargs="?")
    return parser
    #TODO: Create a shell for parser.config to write user_credentials , url, jenkins_path to .env

def create_conf_file():
    lines=["url=http://jenkins-url", "username=username:password", "jenkins_path=/home/user/projects/repo/Jenkinsfile"]
    with open(".env",'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
        f.close()
    return open_conf_file()
    
def open_conf_file():
    if name != 'posix' and os.path.isfile('.env'):
        print("Open the .env file in your virtual environment to configure the Jenkinsfile linter")
    if name == 'posix' and os.path.isfile('.env'):
        print("Opening .env")
        return subprocess.run(['code','.env'], encoding='UTF-8', capture_output=True, text=True).stdout.strip("\n")
    else:
        return create_conf_file()

def jenkins_client():
    if os.path.isfile("jenkins-cli.jar"):
        print("Jenkins-client found")
    else:
        print("Jenkins-client not found\n jklint is going to download jenkins-cli.jar from your Jenkins server")
        r = get("{}/jnlpJars/jenkins-cli.jar".format(config['url']))
        open('jenkins-cli.jar', 'wb').write(r.content)
def main():
    
    from time import sleep
    import dotenv
    import jklint.call as call, jklint.cli as cli

    parser = create_parser()
    args = parser.parse_args()
    if args.config == 'config':
        return open_conf_file()
    if args.config == 'go':
        jenkins_client()
        sleep(2)
        return call.lint()