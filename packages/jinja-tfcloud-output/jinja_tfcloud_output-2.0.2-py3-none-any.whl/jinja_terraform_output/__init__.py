__version__ = '1.0.5'
__author__ = 'lummo-io'

import json
import os
import requests
from urllib.parse import urljoin

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.nodes import Const
from pathlib import Path

# Required inputs
# - org_name, workspace_name, state_output_name
# This class is an extension to the jinja2 templating engine that allows you to access the outputs of
# a terraform workspace
class TerraformQueryExtension(Extension):
    tags = {'terraform_query'}

    def parse(self, parser):
        line_number = next(parser.stream).lineno

        ORGANIZATION = os.getenv("ORGANIZATION", None)
        WORKSPACE = os.getenv("WORKSPACE", None)
        
        name = parser.parse_expression()
        parser.stream.skip_if('comma')

        org_name = nodes.Const(ORGANIZATION)
        workspace_name = nodes.Const(WORKSPACE)
        value_name = nodes.Const(None)

        if parser.stream.skip_if('name:organization'):
            parser.stream.skip(1)
            org_name = parser.parse_expression()

        if parser.stream.skip_if('name:workspace'):
            parser.stream.skip(1)
            workspace_name = parser.parse_expression()

        if parser.stream.skip_if('name:value_name'):
            parser.stream.skip(1)
            value_name = parser.parse_expression()

        if (not isinstance(org_name, nodes.Const)) or (not org_name.value):
            parser.fail("Organization not specified", lineno=line_number)
        
        if (not isinstance(workspace_name, nodes.Const)) or (not workspace_name.value):
            parser.fail("Workspace not specified", lineno=line_number)

        if (not isinstance(value_name, nodes.Const)):
            parser.fail("Value is not of type nodes.const", lineno=line_number)

        args = (name, org_name, workspace_name, value_name)

        return nodes.Output(
            [self.call_method('_access_state_output', args)], lineno=line_number
        )
    
    def _access_state_output(self, name, org_name, workspace_name, value_name):
        return self._get_outputs(name, org_name, workspace_name, value_name)
    
    # get org and workspace from env variables but prefer invocation vars
    def _get_outputs(self, name, org_name, workspace_name, value_name):
        TFC_TOKEN = os.getenv('TFC_TOKEN', None)
        # Reading the token from the credentials.tfrc.json file if ENV not present.
        if TFC_TOKEN is None:
            try:
                with open(f'{Path.home()}/.terraform.d/credentials.tfrc.json', 'r') as f:
                    config = json.load(f)
                    TFC_TOKEN = config['credentials']['app.terraform.io']['token']
            except FileNotFoundError:
                print("Couldn't find file")      

        headers = {
            "Authorization": f"Bearer {TFC_TOKEN}",
            "Content-Type": "application/vnd.api+json"
        }

        # Getting the current state version outputs for the workspace.
        TFC_URL = 'https://app.terraform.io/'
        BASE_URL = urljoin(TFC_URL, "/api/v2")
        ORG_PATH = urljoin("/organizations/", org_name)
        WORKSPACE_PATH = urljoin("/workspaces/", workspace_name)
        workspace_url = urljoin(BASE_URL, ORG_PATH, WORKSPACE_PATH)
        s = requests.Session()
        s.headers.update(headers)
        resp = s.get(workspace_url)
        search_listed_ws = resp.json()
        ws_id = search_listed_ws['data']['id']
        state_output_path = urljoin("/workspaces/", ws_id, "/current-state-version-outputs")
        state_output_url = urljoin(BASE_URL, state_output_path)
        resp = s.get(state_output_url)
        current_state_version_outputs = resp.json()
        current_state_version_outputs = current_state_version_outputs["data"]
        
        # Iterating over the outputs and returning the value of the output with the name that matches the name
        # passed in.
        for output in current_state_version_outputs:
            if(output["attributes"]["name"] == name):
                if(value_name is not None):
                    return output["attributes"]["value"][value_name]
                return output["attributes"]["value"]
