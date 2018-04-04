import urllib2
import webbrowser
import poster.encode
import poster.streaminghttp
import json

login_url = "http://127.0.0.1:8000/workflowFile_add/"
fileName = 'workflow.json'
opener = poster.streaminghttp.register_openers()

params =  dict(json=open(fileName, 'rb'))
datagen, headers = poster.encode.multipart_encode(params)
response = opener.open(urllib2.Request(login_url, datagen, headers))

_dict = json.loads(response.read())

login_url = "http://127.0.0.1:8000/workflowModel_add/"
fileNameUrl = "?jsonFileName=%s"%_dict['jsonFileName']
webbrowser.open(login_url+fileNameUrl)


