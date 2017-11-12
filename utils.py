import requests
import shutil


def web_get(src_url: str, dest: str):
    """Download image from the Medium server"""

    req = requests.get(src_url, stream=True)
    if req.status_code == 200:
        with open(dest, 'wb') as res_fi:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, res_fi)
