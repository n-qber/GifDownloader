import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import urllib.parse
import json
from my_library import mThreading
import requests


class Authenticate:
    def __init__(self, credentials_json='client_secret.json', permissions=['https://www.googleapis.com/auth/youtube.upload'], redirect_uri=None):
        """
        Actually i don't remember how this works because oauth is a little complicated
        and i had forgotten to do a step one time so, yep, i'm more confused than you
        but it works with all the steps ok

        Just know that in the api you should use the urls:

        http://localhost:5000/

        and the redirect:

        http://localhost:5000/oauth2callback

        :param credentials_json: the client secret file from the google oauth api
        :param permissions: well what you will want to do with your program (i know this repository is just for reposting but idc, i might want to use it for another thing)
        :param redirect_uri: i dont remember what this does but i think it is this: http://localhost:5000
        """
        self.credentials_json = credentials_json
        self.permissions = permissions
        self.redirect_uri = redirect_uri

        if self.redirect_uri is None:
            with open(self.credentials_json, "r") as credentials_json_file:
                self.redirect_uri = json.load(credentials_json_file)["web"]["redirect_uris"][0]

        self.app = flask.Flask(__name__)

    def start(self):

        authorization_url, state = self.get_authorization_url()

        @self.app.route('/')
        def bar():
            return flask.redirect(authorization_url)

        @self.app.route('/oauth2callback')
        def oauth2callback():

            with open("code.json", "w") as token_json:
                args = flask.request.args.to_dict()
                args['url'] = flask.request.url
                token_json.write(json.dumps(args))

            return flask.request.args

    def get_authorization_url(self):

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.credentials_json,
            self.permissions)

        flow.redirect_uri = self.redirect_uri

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
        print(authorization_url)
        return authorization_url, state

    @staticmethod
    def credentials_to_dict(credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}

    def exchange_code(self):
        """
        with open("code.json", "r") as token_json:
            codes = json.load(token_json)

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.credentials_json, scopes=self.permissions, state=codes['state'])

        flow.redirect_uri = self.redirect_uri
        authorization_response = codes['url']
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        values = {'credentials': Authenticate.credentials_to_dict(credentials)}

        with open('token.json', 'w') as token:
            token.write(json.dumps(values))

        return values
        """
        with open("code.json", "r") as token_json:
            code = json.load(token_json)["code"]
        with open(self.credentials_json, "r") as credentials:
            credentials_dict = json.load(credentials)
            client_id = credentials_dict["web"]["client_id"]
            client_secret = credentials_dict["web"]["client_secret"]
            redirect_uri = credentials_dict["web"]["redirect_uris"][0]
            print(redirect_uri)

        data = dict(
            grant_type="authorization_code",
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )

        req = requests.post("https://accounts.google.com/o/oauth2/token", data=data)
        with open("token.json", "wb") as token:
            token.write(req.content)

        return req.content

    @mThreading.thread
    def run(self, host, port):
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    auth = Authenticate(permissions=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    auth.start()
    auth.run('localhost', 5000)
