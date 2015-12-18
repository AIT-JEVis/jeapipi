from jeapipy.jeapi import JEVisConnector

server = "http://localhost:8080/JEWebService/v1"
user = "Sys Admin"
password = "jevis"

con = JEVisConnector(server, user, password)

if not con.isConnected():
  print("Error: could not connect to server")
  exit(1)

print("Connected to JEVis3 WebService!")

# get the Organization Directory
organizationDir = con.getObject(root="false", jclass="Organization Directory")

# Print all Organizations
for childID in con.getChildren(organizationDir['Object']['id']):
  child = con.getObjectByID(childID)
  print('name:', child['name'])
  print('jevisclass:', child['jevisclass'])

