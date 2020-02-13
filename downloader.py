import requests
from urllib.request import urlretrieve
import re

class Downloader:
    def __init__(self):
        pass
    
    @staticmethod
    def student_url(url, filename=False):
        res = requests.get(url)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)
        download_url = links[1]
        if download_url.startswith("http://resizeimage.net"):
            return "expired"
        if filename:
            urlretrieve(download_url, filename)
        else:
            return res.content


