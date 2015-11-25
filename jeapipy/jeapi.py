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

    def getSeperator(self, query):
            if query:
                return "&"
            else:
                return "?"
                
                
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


    def query(self, query):
        url = self.SERVER + query
        print("url: ", url)
        self.R = requests.get(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R.json()
        
    def getLastRequest(self):
        return self.R

    def getStatusCode(self):
        # TODO: error handling
        if self.R == None:
            return 0
        return self.R.status_code





    def getObject(self, root=None, jclass=None, inherit=None, name=None,detail=None, parent=None, child=None):
        params = ""
         
        if root:
            params += "{}root={}".format(self.getSeperator(params), root)
        if jclass:
            params += "{}class={}".format(self.getSeperator(params), jclass)
        if inherit:
            params += "{}inherit={}".format(self.getSeperator(params), inherit)
        if name:
            params += "{}name={}".format(self.getSeperator(params), name)
        if parent:
            params += "{}parent={}".format(self.getSeperator(params), parent)
        if child:
            params += "{}child={}".format(self.getSeperator(params), child)
        
        query = "/objects{}".format(params)
        return self.query(query)
        
    def getObjectByID(self, id, detail=None):
        params = ""
         
        if detail:
            params += "{}detail={}".format(self.getSeperator(params), detail)
        
        query = "/objects/{}{}".format(id,params)
        return self.query(query)
        
        
    def getAttributes(self, id):
        query = "/objects/{}/attributes".format(id)
        return self.query(query)
    
    def getAttribute(self, id, attribute):
        query = "/objects/{}/attributes/{}".format(id, attribute)
        return self.query(query)
        
    # "yyyyMMdd'T'HHmmss
    def getSamples(self, id, attribute="Value", start=None, end=None, onlyLatest=None):
        params = ""
         
        if start:
            params += "{}from={}".format(self.getSeperator(params), start)
        if end:
            params += "{}until={}".format(self.getSeperator(params), end)
        if onlyLatest:
            params += "{}onlyLatest={}".format(self.getSeperator(params), onlyLatest)

        query = "/objects/{}/attributes/{}/samples{}".format(id, attribute, params)
        return self.query(query)
      
      
      
      
      
      

    

      
    def deleteObject(self, id):
        url = self.SERVER + "/objects/{}".format(id)
        print("url: ", url)
        self.R = requests.delete(url, auth=self.AUTH)
        
        # TODO: error handling
        return self.R

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
                if rel['from'] != id:
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


