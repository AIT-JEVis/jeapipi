from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import requests
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth

class JEVisConnector:
    """Helper to connect to the JEVis v1 REST-API"""
    def __init__(self, _server, _user, _password):
        """Create the connector"""
        # TODO: sanity check operators
        self.SERVER = _server
        self.USER = _user
        self.PASSWORD = _password
        self.R = None
        self.AUTH = HTTPBasicAuth(self.USER, self.PASSWORD)

    def isConnected(self):
        """check if the JEVis-REST-API is available"""
        url = self.SERVER + "/objects"
        try:
            self.R = requests.get(url, auth=self.AUTH)
        
            return self.R.status_code == 200
        except ConnectionError as e:
            self.R = None
            print("Connection Failed, Exception: ", e)
            return 0

    def getLastRequest(self):
        return self.R

    def getStatusCode(self):
        # TODO: error handling
        if self.R == None:
            return 0
        return self.R.status_code

    def getObject(self, id):
        url = self.SERVER + "/objects/{}".format(id)
        print("url: ", url)
        self.R = requests.get(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R.json()

    def deleteObject(self, id):
        url = self.SERVER + "/objects/{}".format(id)
        print("url: ", url)
        self.R = requests.delete(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R

    def getObjectQuery(self, id, query):
        url = self.SERVER + "/objects/{}".format(id)
        url += query
        print("url: ", url)
        self.R = requests.get(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R.json()

    def getClassObjects(self, className):
        url = self.SERVER + "/objects"
        url += '?class={}&inherit=false&root=false'.format(className)
        print("url: ", url)
        self.R = requests.get(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R.json()

    def getChildren(self, id):
        """get a list of children of the given id"""
        url = self.SERVER + "/objects"
        url += '/{}'.format(id)
        print("url: ", url)
        self.R = requests.get(url, auth=self.AUTH)
        
        data = self.R.json()
        rels = data['relationships']

        children = []
        for rel in rels:
            if rel['type'] == '1':
                # type 1, to parent, from child
                #print("to: ", rel['to'], " from: ", rel['from'])
                children.append(rel['from'])
        return children

    def getLatestFile(self, id, attribute, filename=None):
        url = self.SERVER + "/objects"
        url += '/{}'.format(id)
        url += '/attributes/{}'.format(attribute)
        url += '/samples/Files?onlyLatest=true'
        
        self.R = requests.get(url, auth=self.AUTH)
        f = dict()
        f['name'] = self.R.headers['Content-disposition'].split("filename=")[1].strip('"')
        f['content'] = self.R.content

        if filename == None:
            filename = f['name']

        file_out = io.open(filename, 'wb')
        file_out.write(f['content'])
        file_out.close()
        return f

    def uploadFile(self, id, attribute, filename, remote_filename=None):
        url = self.SERVER + "/objects"
        url += '/{}'.format(id)
        url += '/attributes/{}'.format(attribute)
        url += '/samples/Files'
        
        # prepare file and set remote filename
        if remote_filename == None:
            remote_filename = os.path.basename(filename)
        files = {'file': (remote_filename, io.open(filename, 'rb'))}

        # upload file
        self.R = requests.post(url, files=files, auth=self.AUTH)
        return self.R


