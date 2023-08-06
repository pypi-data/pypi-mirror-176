import urllib
import tqdm
import pymongo
import math
import sys
import os
from pydantic import BaseSettings
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import applications

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Database Name
db = client["phishingdetector"]
# Collection Name
col = db["searchengine"]


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch


# Global variables for API Result
class Settings(BaseSettings):
    data: list = []
    distinct_names: list = []
    url: str = ""
    results: str = ""
    verdict: str = ""
    plugins: list = []
    plugins_names: list = []


# Global variables for API is-alive ping
class Update(BaseSettings):
    status: str = "Null"
    error_message: str = ""


settings = Settings()
update = Update()


# Retrieve Data from Database
def getData(url):
    # Remove https:// and http://
    url2 = url.replace("http://", "")
    url2 = url2.replace("https://", "")
    url2 = url2.strip()

    data = []
    for x in col.find({
        "$or": [
            {"URL": {"$eq": url}},
            {"URL": {"$eq": url2}}
        ]
    }, {"_id": 0}):
        data += [(list(x.values())), ]
    return data


def getURLDetails(link):
    # Convert back from unicode
    while "0x5C" in link:
        link = link.replace("0x5C", "/")
    link = urllib.parse.unquote(link)

    # Get the queried results from the database
    settings.data = getData(link)

    # Get the distinct engine names
    settings.distinct_names = getNames()

    # Get the URL Link
    settings.url = link

    # Get the number of passes and fails
    settings.results = getDetails(settings.data)[0]

    # Get the verdict of the URL
    settings.verdict = getDetails(settings.data)[1]

    # Get Plugins
    settings.plugins = []
    getPlugins()

    # Set Status to be finish
    update.status = "Finish"

    return "Done"


def getPlugins():

    sys.path.append("Plugins")
    from core import MyApplication

    path = "C://Users//Russell-Intern//PycharmProjects//pythonProject//pythonProject//Plugins"
    dir_list = os.listdir(path)
    files_list = []

    for file in dir_list:
        if file[len(file) - 3:len(file)] == ".py" and file != "core.py":
            files_list += [file[0:len(file) - 3], ]
    print(files_list)

    app = MyApplication(files_list)
    # Run our application
    app.run()


def split_into(n, p):
    split = ([n / p + 1] * (n % p) + [n / p] * (p - n % p))
    split_values = []
    count = 0
    for i in range(p):
        split_values += [count, ]
        count += math.floor(split[i])
    split_values += [n, ]
    return split_values


def insertThread(content_assignment, length):
    # today = datetime.now()
    # print("The time is: " + str(today))
    for i in tqdm(range(length)):
        name = content_assignment[i]
        name = name.split(b',')

        if update.error_message != "":
            print("Fail")
            return "Fail"

        if len(name) == 1 and len(name[0]) == 0:
            print("Ignore blank lines")
        else:
            # This is to ensure the file provided follows the format of {Engine Name}, {URL}, {Result}, {Details}
            if len(name) == 4:
                for i in range(4):
                    name[i] = name[i].decode().strip()
                insertData(name)

            else:
                # The format provided in the file is wrong [FILE FORMAT CHECK]
                for i in range(len(name)):
                    name[i] = name[i].decode().strip()
                update.error_message = "Invalid File Format. " + str(name)
    return "Success"


# Checks for number of unique URLs
def checkURL(data):
    URLs = []
    for i in range(len(data)):
        # Loop through for each row of data returned
        if data[i][3] not in URLs:
            # Get the list of Unique URLs
            URLs += [data[i][1], ]
    return URLs


# Get the verdict of the URL
def getDetails(data):
    total = getTest(data)
    result = str(total[1]) + " / " + str(total[0])
    verdict = "This URL has been flagged as safe to be used from checking our databases"
    if total[0] == 0 and total[1] == 0:
        verdict = "This URL does not exist in our database"
    elif 0.5 <= total[1] / total[0] < 0.7:
        # If number of failed tests is 30% - 50%
        verdict = "This URL has been flagged by a minority of our databases. Proceed with caution"
    elif total[1] / total[0] < 0.5:
        # If number of failed tests is more than 50%
        verdict = "This URL has been flagged by a majority of our databases. You are advice to not visit this link"

    return [result, verdict]


# Get number of pass and fail
def getTest(data):
    failed = 0
    passed = 0

    for i in range(len(data)):
        print(data[i][2])
        if data[i][2] == "Fail":
            failed += 1
        elif data[i][2] == "Success":
            passed += 1
    print("The number of pass is: " + str(passed))
    total = failed + passed
    output = [total, passed]
    return output


# Insert Data into Database
def insertData(data):
    mydict = {"Engine": str(data[0]), "URL": str(data[1]).replace("www.", ""), "Result": str(data[2]),
              "Details": str(data[3])}
    col.insert_one(mydict)


# Get all unique names of search engines
def getNames():
    x = col.aggregate([{"$group": {"_id": '$Engine'}}])
    data = []
    for engine in x:
        data += [list(engine.values()), ]
    return data
