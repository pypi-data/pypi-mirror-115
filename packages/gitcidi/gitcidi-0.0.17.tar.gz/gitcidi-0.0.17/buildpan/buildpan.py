
"""
    Title: buildpan
    Module Name: buildpan
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ##  Main operating file for all the cli commands             ## 
         ###############################################################
 """
import git
import os
import click
import git

from github import Github
from commands import auth
from commands import allrepo
from commands import selectrepo
# from commands import pull
import sys
# sys.path.append("./buildpan/commands")
import commands.pull
# from commands import webhook




def main():
    buildpan()

@click.group(help="CLI tool to manage full development cycle of projects")
def buildpan():
    pass


@buildpan.command()
# @click.option('--token', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
def print():
    """Authenticate your self"""
    print(auth.tk2)


@buildpan.command()
# # @click.option('--token', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
@click.option('--folder',  prompt='Enter directory name ', help='Shows all the repo in the account')
@click.option('--path',  prompt='Enter path name ', help='Shows all the repo in the account')

def pull(folder,path):
    """Roll back to the previous version"""
    '''
       
    '''
    os.chdir(path)
    # folder=input("Enter the path")
    repo = git.Repo(folder)
    origin = repo.remote(name='origin')
    origin.pull()

buildpan.add_command(auth.auth)
buildpan.add_command(allrepo.allrepo)
buildpan.add_command(selectrepo.selectrepo)
# buildpan.add_command(commands.pull.pulls)

# buildpan.add_command(reset.reset)
# buildpan.add_command(webhook.create_webhook)
if __name__ == '__main__':
    main()
    


