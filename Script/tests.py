import urllib2
import webbrowser
import poster.streaminghttp
import json


def uploadWorkflow(upload_file_url, upload_metadata_url, jsonFileName):
    """ Upload workflow 'jsonFileName'to server upload_file_url
        First the file is uploaded, then the metadata is uploaded.
        The script uploads the file and then opens a browser for the metadata
         Note that the two steps are needed since noinitial value can be passed
         to a file field. poster module is needed. Poster is pure python
         so it may be added to the directory rather than installed if needed.

         The server is django a uses filefield and csrf_exempt.
         csrf_exempt disable csrf checking. filefield
    """
    # json file to upload
    params =  dict(json=open(jsonFileName, 'rb'))
    #we are going to upload a file so this is a multipart connection
    datagen, headers = poster.encode.multipart_encode(params)
    opener = poster.streaminghttp.register_openers()
    #create request and connect to server
    response = opener.open(urllib2.Request(upload_file_url, datagen, headers))
    # server returns dictionary as json with remote name of the saved file
    _dict = json.loads(response.read())
    # server has stored file in file named _dict['jsonFileName']
    fileNameUrl = "?jsonFileName=%s&versionInit=%s"%\
                  (_dict['jsonFileName'], '1.2') # use GET
    # open browser to fill metadata, fileNAme will be saved as session variable
    # note that I cannot save the file nave in the session in the first
    # conection beacause the broeser changes from urlib2 to an actual browser
    # so sessions are different
    webbrowser.open(upload_metadata_url+fileNameUrl)

if __name__ == "__main__":
    print("main")
    upload_file_url = "http://127.0.0.1:8000/workflowFile_add/"
    upload_metadata_url = "http://127.0.0.1:8000/workflowModel_add/"
    jsonFileName = 'workflow.json'

    uploadWorkflow(upload_file_url, upload_metadata_url, jsonFileName)
