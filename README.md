# fastAPI-Mongodb-task-API

## The key features are:
1) Add Task  (Add task name & due date)
2) Delete Task  
3) Update a Task (This can include marking the task as complete or  updating the due date)
4) View a Task 
5) Share task with another user using their email 

Project Organization
------------

    .
    ├── app.py                      > Main file which contains all the functionality to run the API and save the task data into MongoDB database.
    ├── config.json                 > Enviornment file storing all required enviornment variables 
    ├── FastAPI - Swagger UI.pdf    > Demo of the API, to give evidence of it's working
    ├── README.md                   > The top-level README for developers using this project.
    ├── requirements.txt            > All the requirements which is needed to run this project.
    ├── src
    ├── mail.py                     > To share task with another user using their email.
    └── __pycache__
        └── mail.cpython-37.pyc


--------
## Testing

  - This can run on Windows / Linux(Ubuntu 20.04) system.
  - It is advised to create a virtual enviornment if you have existing conflicts with python & other libraries/packages installtions.

## How to replicate project in your system ?

  - Make sure you have updated your OS to latest version.
  - Install all necessary dependencies for this project from requirements.txt
    - Run `pip install -r requirements.txt` for installing dependencies. 
  - Please change parameters accordingly in (config.json) config file as per your system configuration before running the app.py file.
  - Run app.py file in for turn on the API.
    - Run `uvicorn main:app --reload`
  - open http://127.0.0.1:8000/docs on browser to check the Swagger UI.
  - Use logs folder for checking logs related to project.
