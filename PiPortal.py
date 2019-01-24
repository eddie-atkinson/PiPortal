"""
@author: Eddie Atkinson
@version: 0.1
@date: 07/01/18

"""
from flask import Flask, request, jsonify
import requests
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
cardURL = "https://auth.uwamakers.com/api/card"
token = config["setup"]["token"]
context = ("host.cert", "host.key")
"""
Method that takes the uid string provided by the ESP converts the hexadecimal string to an array 
of 4 digits.
"""
def uidSplitter(uid):  
    if(len(uid) != 8):
        print("UID length is wrong")
        return(-1)
    byteArray = []
    for i in range(1,8,2):
        byte = int(uid[i-1 : i+1], 16)
        byteArray.append(byte)
    return(byteArray)
"""
Method that takes a UWA student or staff number and a permision as an argument,
sends a GET request to the auth endpoint requesting all student numbers that have
that permission and testing the username provided for membership of that list. 
Returns 1 if the username provided is present in list of users with the permission, 
0 otherwise. If the user list is empty (i.e. the permission doesn't exist or is unused),
returns -2.
"""

def checkPermission(username, perm):
    permURL = "https://auth.uwamakers.com/api/users/?perm="
    permURL += perm + "&token=" + token + "&csv=true"
    permRequest = requests.get(permURL)
    userList = permRequest.text
    if not userList:
        return(-2)
    elif username in userList:
        return(1)
    else:
        return(0)     

app = Flask(__name__)
@app.route("/card", methods = ["POST"])
def post():
    postRequest = request.form
    uid = postRequest["uuid"]
    permission = postRequest["permission"]
    byteArray = uidSplitter(uid)
    PARAMS = {"token" : token, "uuid": byteArray}
    detailsRequest = requests.post(url = cardURL, params = PARAMS)
    response = detailsRequest.json()
    username = response['user']['username']
    status = checkPermission(username, permission)
    print(status)
    return("Success: " + str(status))

app.run(host="0.0.0.0", port = 8090, ssl_context =  context)

