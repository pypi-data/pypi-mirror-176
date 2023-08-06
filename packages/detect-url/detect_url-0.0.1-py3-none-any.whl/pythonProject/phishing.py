import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from typing import List
import starlette.status as status
from starlette.responses import RedirectResponse
from threading import Thread
import concurrent.futures
from settings import *


app = FastAPI()

templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="Static"), name="static")
app.mount("/css", StaticFiles(directory="CSS"), name="css")


@app.get('/check')
def hello_world():
    return {'message': 'hello'}


# This link to retrieve the JSON Data from Database
@app.get("/Data/{link}")
async def read_item(link: str):

    if update.status == "Null":
        # Set to loading
        print("Set to load")
        update.status = "Loading"
        daemon = Thread(target=getURLDetails, args=(link,), daemon=True, name='Background')
        daemon.start()
        return update.status

    elif update.status == "Loading":
        # Do nothing if status is still Loading
        print("Loading...")
        return update.status

    elif update.status == "Finish":
        # Once Finish, change status back to Null
        print("The function has finished")
        update.status = "Null"
        return settings


# This link is the home page
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


# This link is the URL Details
@app.get("/{url}", response_class=HTMLResponse)
async def read_item(request: Request, url: str):
    return templates.TemplateResponse("frontpage.html", {"request": request, "url": url})


# This link is to upload to the database 
@app.get("/Upload/File", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# This link is for successful SQL Database Uploads          
@app.get("/Upload/Success", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


# This link is for successful SQL Database Uploads          
@app.get("/Upload/Failure/{Message}", response_class=HTMLResponse)
async def read_item(request: Request, Message: str):
    return templates.TemplateResponse("failure.html", {"request": request, "Message": Message})


#  This link is to post the data into SQL
@app.post("/ReadFile")
async def handle_form(files: List[UploadFile] = File(...)):
    min_file = 0
    max_file = 5
    max_size = 10000000
    accept_files = ["text/plain", "application/vnd.ms-excel"]

    # Ensure at least one file was submitted [NO. OF FILES CHECK]
    if len(files) == min_file:
        message = "Please submit a minimum of one file"
        return RedirectResponse(
            '/Upload/Failure/' + message,
            status_code=status.HTTP_302_FOUND)

    # Accept a maximum of five files [NO. OF FILES CHECK]
    elif len(files) > max_file:
        message = "Please submit a maximum of five files"
        return RedirectResponse(
            '/Upload/Failure/' + message,
            status_code=status.HTTP_302_FOUND)

    else:
        # Loop through each file
        for i in range(len(files)):

            content_assignment = await files[i].read()
            content_assignment = content_assignment.split(b'\n')
            update.error_message = ""

            # Ensure it is no bigger than 10,000KB [FILE SIZE CHECK]
            if len(content_assignment) > max_size:
                message = "Invalid File Size. Please submit a file size less than 10,000KB"
                return RedirectResponse(
                    '/Upload/Failure/' + message,
                    status_code=status.HTTP_302_FOUND)

            else:

                # Check if the file type submitted is valid [FILE TYPE CHECK]
                if files[i].content_type in accept_files:

                    length = len(content_assignment)
                    # The number of threads to start
                    no_threads = 5

                    # Check the number of lines is less than number of threads
                    if length < no_threads:
                        no_threads = length

                    values = split_into(length, no_threads)

                    list1 = []
                    list2 = []

                    for i in range(no_threads):
                        split_content_assignment = content_assignment[values[i]:values[i + 1]]
                        difference = values[i + 1] - values[i]

                        list1 += [split_content_assignment, ]
                        list2 += [difference, ]

                    with concurrent.futures.ThreadPoolExecutor(max_workers=no_threads) as executor:
                        future = executor.map(insertThread, list1, list2)

                else:
                    message = "Invalid File Type. Please submit a .txt or .csv file"
                    return RedirectResponse(
                        '/Upload/Failure/' + message,
                        status_code=status.HTTP_302_FOUND)

    if update.error_message != "":
        return RedirectResponse(
            '/Upload/Failure/' + update.error_message,
            status_code=status.HTTP_302_FOUND)
    else:

        return RedirectResponse(
            '/Upload/Success',
            status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run(app)
