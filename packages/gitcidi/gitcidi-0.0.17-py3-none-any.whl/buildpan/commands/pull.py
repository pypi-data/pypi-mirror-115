
"""
    Title: reset.py
    Module Name: reset.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 05-07-2021
    Description:
        ###############################################################
        ## Reset/ rollback function     ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
# from github import Github
from git import Repo

# import glob
# # for taking the path
# path=input("Enter the path ")

# os.chdir(path)
# # dir=os.path.dirname(path)

# # matching the extension 
# ext="csv"
@click.command()
@click.option('--folder', '-e', default="dev", prompt='Enter token ', help='Shows all the repo in the account')
def pull(folder):
    """Roll back to the previous version"""
    '''
       
    '''
    # os.chdir(path)
    # folder=input("Enter the path")
    repo = git.Repo(folder)
    origin = repo.remote(name='origin')
    origin.pull()

# Repo.clone_from("https://github.com/AkashAi7/demosession1.git", "clone")

