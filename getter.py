from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
import httplib2
import numpy as np
from downloader import Downloader
from os import mkdir

import json


class Getter:
    def __init__(self, spread_sheet_id, creds_filename="token.json"):
        self.spread_sheet_id = spread_sheet_id

        with open("client_secret.json") as cj:
            client_secrets = json.load(cj)

        with open(creds_filename, "r") as creds_file:
            token_secrets = json.load(creds_file)

        creds = OAuth2Credentials(
            token_secrets["access_token"], client_secrets["web"]["client_id"], client_secrets["web"]["client_secret"],
            token_secrets["refresh_token"], token_secrets["expires_in"], "https://accounts.google.com/o/oauth2/token", "", scopes=token_secrets["scope"])

        self.viewer = build('sheets', 'v4', credentials=creds)
        self.sheet = self.viewer.spreadsheets()

    def get_values(self):
        result = self.sheet.values().get(spreadsheetId=self.spread_sheet_id, range="A1:Z4").execute()
        return result.get('values', [])
    
    def download_all(self):
        for hour, name, cless, link in self.get_values()[1:]:
            try:
                mkdir("media/" + cless)
            except:
                pass
            Downloader.student_url(link, "media/" + cless + "/" + name + ".gif")


