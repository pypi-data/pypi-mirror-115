import git
import os
import click
import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from github import Github
import yaml 
ENDPOINT = "webhook"

# a_yaml_file = open("./configdemo.yaml")
# parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

# username=parsed_yaml_file["user_name"]
# token=parsed_yaml_file["access_token"]
@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
)
class PayloadView():
    # this class will called automatically when webhook will be created successfully on a repository

    def __init__(self, request):
        self.request = request
        self.payload = self.request.json

    # This method will be called when webhook will be created successfully on a repository
    @view_config(header="X-GitHub-Event:ping")
    def payload_ping(self):
        print("Pinged! Webhook created with id {}!".format(self.payload["hook_id"]))
        return {"status": 200}

    # This method will be called when an particular push event will be triggered on an repository
    @view_config(header="X-Github-Event:push")
    def payload_push(self):
        print("No. of commits in push: ", len(self.payload['commits']))
        print("commit msg", self.payload["commits"][0]["message"])
        print("commit added", self.payload["commits"][0]["added"])
        return Response("success")

    # This method will be called when an pull request will be happen on a repository
    @view_config(header="X-GitHub-Event:pull_request")
    def payload_pull_request(self):
        print("pull request = ", self.payload['action'])
        print("commits in pull: ", self.payload['pull_request'])
        return Response("success")


# create webhook on a particular repo
@click.command()
@click.option('--path', '-e', default="config file ", prompt='Enter the path ', help='Enter the username of ')
@click.option('--host', '-e', default="host file ", prompt='Enter the host  ', help='enter the host ')
def create_webhook(path,host):

    os.chdir(path)
    a_yaml_file = open("./config.yaml")
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    username=parsed_yaml_file["user_name"]
    token=parsed_yaml_file["access_token"]
    access_token = token# "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"
    OWNER = username#"AkashAi7" # github account name
    REPO_NAME = "demosession1"# github repository name
    EVENTS = ["*"]      # Events on github
    HOST = host#"343328894880.ngrok.io"  # ngrok tunnel
    config = {
        "url": "http://{host}/{endpoint}".format(host=HOST, endpoint=ENDPOINT),
        "content_type": "json"
    }

     # login to github account
    g = Github(access_token)

    # accessing a particular repository of a account
    repo = g.get_repo("{owner}/{repo_name}".format(owner=OWNER, repo_name=REPO_NAME))
    print(repo)

    # creating a webhook on a particular repository
    repo.create_hook("web", config, EVENTS, active=True)

   


if __name__ == "__main__":
    config = Configurator()

    config.add_route(ENDPOINT, "/{}".format(ENDPOINT))
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("localhost", 80, app)
    create_webhook()
    server.serve_forever()



