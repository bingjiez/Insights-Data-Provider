import os
from os import path
from dotenv import load_dotenv
import requests
import pandas as pd
import sys, getopt

def getAccessToken(token_url, client):
    if(token_url == None or client == None):
        return None
    response = requests.post(token_url, data=client)
    if(response.status_code != requests.codes.ok):
        print("Error: {0}".format(response))
        return None
    return response.json()['access_token']

def getGroups(access_token, base_url, reportId):
    headers = {
        "Authorization": 'Bearer ' + access_token,
        "Accept": "application/vnd.bentley.itwin-platform.v1+json",
    }

    groups_url = base_url + '/' + reportId
    response = requests.get(groups_url, headers=headers)
    if(response.status_code != requests.codes.ok):
        print("Error: {0}".format(response))
        return None

    groupList = response.json()['value']
    if (groupList == None):
        print("Error: {0}".format(response))
        return None
    print(str(len(groupList)) + " groups in the report")

    groups = []
    for group in groupList:
        group_name = group['name']
        group_url = groups_url + '/' + group['url']
        response = requests.get(group_url, headers=headers)
        if (response.status_code != requests.codes.ok):
            print("Error: {0}".format(response))
            return None

        page = response.json()
        if(page == None):
            print("Error: {0}".format(response))
            return None
        currentGroup = {
            'name': '_'.join(group_name.split('_')[1:-2]),
            'properties': page['value']
        }
        while ("@odata.nextLink" in page.keys()):
            response = requests.get(page["@odata.nextLink"], headers=headers)
            if(response.status_code != requests.codes.ok):
                print("Error: {0}".format(response))
                return None

            page = response.json()
            if (page == None):
                print("Error: {0}".format(response))
                return None
            if(page['value'] != None):
                currentGroup['properties'] += page['value']
        groups.append(currentGroup)
        print("Added group: " + currentGroup['name'])
    return groups

def flattenGroups(groups):
    rows = []
    for group in groups:
        if(len(group['properties']) == 0):
            continue
        for prop in group['properties']:
            prop['class'] = group['name']
            rows.append(prop)
    return rows

def printUsage():
    print('python data.py -o <outputfile>')

def main(argv):
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"ho:",["outputFile="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            printUsage()
            sys.exit()
        elif(opt in ("-o", "--outputfile")):
            outputfile = arg

    if(not outputfile):
        print("Unsupported usage")
        printUsage()
        sys.exit(2)

    load_dotenv()

    # Authorization
    token_url = os.getenv('TOKEN_URL') if os.getenv('TOKEN_URL') else "https://ims.bentley.com/connect/token"
    grant_type = os.getenv('GRANT_TYPE') if os.getenv('GRANT_TYPE') else 'client_credentials'
    scope = os.getenv('SCOPE') if os.getenv('SCOPE') else "insights:read insights:modify"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    client = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": grant_type
    }
    access_token = getAccessToken(token_url, client)
    if(access_token == None):
        sys.exit()

    # Retrieve data
    base_url = os.getenv('BASE_URL') if os.getenv('BASE_URL') else "https://api.bentley.com/insights/reporting/odata/"
    reportId = os.getenv('REPORT_ID')

    groups = getGroups(access_token, base_url, reportId)
    df = pd.DataFrame(flattenGroups(groups))

    print("Saving data")
    df.to_csv(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])