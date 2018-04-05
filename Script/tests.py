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
    opener = poster.streaminghttp.register_openers()

    params =  dict(json=open(jsonFileName, 'rb'))
    datagen, headers = poster.encode.multipart_encode(params)
    response = opener.open(urllib2.Request(upload_file_url, datagen, headers))

    _dict = json.loads(response.read())

    fileNameUrl = "?jsonFileName=%s"%_dict['jsonFileName'] # use GET
    webbrowser.open(upload_metadata_url+fileNameUrl)

if __name__ == "__main__":
    print("main")
    upload_file_url = "http://127.0.0.1:8000/workflowFile_add/"
    upload_metadata_url = "http://127.0.0.1:8000/workflowModel_add/"
    jsonFileName = 'workflow.json'

    uploadWorkflow(upload_file_url, upload_metadata_url, jsonFileName)
