import urllib
import urllib2
import webbrowser
import contextlib
import json

login_url = "http://127.0.0.1:8000/workflowFile_add/"
fileName = '/home/roberto/sda/ScipionUserData/projects/AD41_PDB/workflow.json'
cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)
urllib2.install_opener(opener)

opener.open(login_url)

try:
    token = [x.value for x in cookies.cookiejar if x.name == 'csrftoken'][0]
except IndexError:
    print (False, "no csrftoken")

with open(fileName, 'r') as f:
    content = f.read()

params =  dict(csrfmiddlewaretoken=token,
               json=content,
               jsonFileName='qwerty')
encoded_params = urllib.urlencode(params)

with contextlib.closing(opener.open(login_url, encoded_params)) as f:
    html = f.read()

with open("results.html", "w") as f:
    f.write(html)

#webbrowser.open("file://results.html")


