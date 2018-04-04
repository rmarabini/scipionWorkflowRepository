import requests

upload_file_url = "http://127.0.0.1:8000/workflowFile_add/"
uploadfile = 'workflow.json'

response = requests.post(upload_file_url,
                         files={'json': open(uploadfile,'rb'),
                                'jsonFileName':'qwerty'})
f = open("kk.html","w")
f.write(response.content)
f.close()