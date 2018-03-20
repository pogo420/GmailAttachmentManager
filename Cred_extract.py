import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from json import load

class Cred_extract(object):

    def __init__(self,config_path):

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail_cred.json')

        store = Storage(credential_path)
        self.credentials = store.get()

        with open(config_path) as f:
            json_data = load(f)
            #print(json_data.keys())  # checking keys of config

            CLIENT_SECRET_FILE = json_data.get("CLIENT_SECRET_FILE")
            SCOPES = json_data.get("SCOPES")
            APPLICATION_NAME = json_data.get("APPLICATION_NAME")

            if not self.credentials or self.credentials.invalid:
                flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                self.credentials = tools.run_flow(flow, store)
                print('Storing credentials to ' + credential_path)


if __name__ == "__main__":

    CONFIG = r"../Credentials/config.json"
    Cred_extract(CONFIG)
