# Demonstrates how to create a new site

# For Http calls
import httplib, urllib, json

# For system tools
import sys, os

# For reading passwords without echoing
import getpass

# Defines the entry point into the script
def main(argv=None):
  
    # Ask for admin/publisher user name and password
    username = "siteadmin"
    password = "siteadmin"

    # Ask for server name
    serverName = "localhost"
    serverPort = 6080 

    # Ask for config store and root server directory paths
    rootDirPath = "C:\\ArcGISServer"
    configStorePath = os.path.join(rootDirPath, "configStore")
    
    
    # Set up required properties for config store
    configStoreConnection={"connectionString": configStorePath, "type": "FILESYSTEM"}
 
    # Set up paths for server directories             
    cacheDirPath = os.path.join(rootDirPath, "arcgiscache")
    jobsDirPath = os.path.join(rootDirPath, "arcgisjobs")
    outputDirPath = os.path.join(rootDirPath, "arcgisoutput")
    systemDirPath = os.path.join(rootDirPath, "arcgissystem")
   
    # Create Python dictionaries representing server directories
    cacheDir = dict(name = "arcgiscache",physicalPath = cacheDirPath,directoryType = "CACHE",cleanupMode = "NONE",maxFileAge = 0,description = "Stores tile caches used by map, globe, and image services for rapid performance.", virtualPath = "")    
    jobsDir = dict(name = "arcgisjobs",physicalPath = jobsDirPath, directoryType = "JOBS",cleanupMode = "TIME_ELAPSED_SINCE_LAST_MODIFIED",maxFileAge = 360,description = "Stores results and other information from geoprocessing services.", virtualPath = "")
    outputDir = dict(name = "arcgisoutput",physicalPath = outputDirPath,directoryType = "OUTPUT",cleanupMode = "TIME_ELAPSED_SINCE_LAST_MODIFIED",maxFileAge = 10,description = "Stores various information generated by services, such as map images.", virtualPath = "")
    systemDir = dict(name = "arcgissystem",physicalPath = systemDirPath,directoryType = "SYSTEM",cleanupMode = "NONE",maxFileAge = 0,description = "Stores files that are used internally by the GIS server.", virtualPath = "")
 
    # Serialize directory information to JSON    
    directoriesJSON = json.dumps(dict(directories = [cacheDir, jobsDir, outputDir, systemDir]))      
  
    # Construct URL to create a new site
    createNewSiteURL = "/arcgis/admin/createNewSite"
    
    # Set up parameters for the request
    params = urllib.urlencode({'username': username, 'password': password, 'configStoreConnection': 

configStoreConnection, 'directories':directoriesJSON, 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters    
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", createNewSiteURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while creating the site."
        return
    else:
        data = response.read()
        httpConn.close()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):          
            print "Error returned by operation. " + str(data)
        else:
            print "Site created successfully"
     
        return
    

# A function that checks that the input JSON object 
#  is not an error object.
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True
    
        
# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))