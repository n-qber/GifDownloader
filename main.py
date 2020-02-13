from authenticator import Authenticate
from getter import Getter
from os import mkdir

try:
    mkdir("media")
except:
    pass

if __name__ == '__main__':

    if input("Do you already have the upload code (Y/N):  ").lower().startswith("N"):

        auth = Authenticate(permissions=['https://www.googleapis.com/auth/spreadsheets.readonly'])
        auth.start()
        auth.run('localhost', 5000)
        input("Got credentials? >  ")
        auth.exchange_code()

    getter = Getter("1oZAeSwoj1FJAIDx6ZzlxE5KXxnAy8z2cLAcdQGzMc3E")
    getter.download_all()