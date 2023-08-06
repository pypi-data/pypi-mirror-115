
"""
    Title: auth.py
    Module Name: auth.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Authenticate the user account    ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
# from github import Github
from git import Repo

@click.command()
@click.option('--folder', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
def pull(folder):
    """Roll back to the previous version"""
    # folder=input("Enter the path")
    repo = git.Repo(folder)
    origin = repo.remote(name='origin')
    origin.pull()

    


   
