try:
    from fastapi import FastAPI, BackgroundTasks
    from starlette.requests import Request
    import uvicorn
    from pydantic import BaseModel
    from datetime import date, datetime, time, timedelta
    import json
    import logging
    #MOTOR
    import motor.motor_asyncio
    from bson.objectid import ObjectId
    from src.mail import send_mail
    logging.info('All  Module loaded successfully!!')
except Exception as e:
    logging.info("Error Some Modules are Missing  : {} ".format(e))


with open('config.json', 'r') as config:
    '''
    Extract all parameters from config file.
    '''
    params = json.load(config)["params"]
    # params
    MongoDB_host = params["MongoDB_host"]
    Mail_sender_id = params["Mail_sender_id"]
    Mail_sender_password = params["Mail_sender_password"]
    


MONGO_DETAILS = MongoDB_host
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.FASTAPI
FASTAPI_collection = database.get_collection("FASTAPI_collection")
logging.basicConfig(filename = datetime.today().strftime("%d_%m_%Y"),level = logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Database connected successfully!!')

def task_helper(task) -> dict:
    '''
    helper to make the mongo query into dict form
    '''
    return {
        "id": str(task["_id"]),
        "task_name": task["task_name"],
        "due_date": task["due_date"],
        "done": task["done"]
    }
def write_notification(email, message):
    '''
    Send mail with the task and due date to another mail_id.
    '''
    send_mail(Mail_sender_id, Mail_sender_password, email, message)
    logging.info(f"Notification sent to {email}:\n \t task: {message}")
        

app = FastAPI()

class Items(BaseModel):
    task_name: str
    due_date: str
    done: bool

# Retrieve all tasks present in the database
@app.get("/")
async def get_all_task():
    tasks = []
    async for task in FASTAPI_collection.find():
        tasks.append(task_helper(task))
    return tasks

# Retrieve a task with a matching ID present in the database
@app.get("/{task_id}")
async def get_task(task_id:str):
    task_data = await FASTAPI_collection.find_one({"_id": ObjectId(task_id)})
    return task_helper(task_data)

# Add a new task into to the database
@app.post('/new/')
async def post_task(item: dict) -> dict:
    task_data = await FASTAPI_collection.insert_one(item)
    new_task = await FASTAPI_collection.find_one({"_id": task_data.inserted_id})
    return task_helper(new_task)


# Delete a task from the database
@app.delete('/delete_task/{task_id}')
async def delete_task(task_id: str):
    '''
    Return: 
            true, once the task got deleted.
    '''
    task = await FASTAPI_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        await FASTAPI_collection.delete_one({"_id": ObjectId(task_id)})
        return True
    return False

# Update task with a matching ID
@app.put('/update_task/{task_id}')
async def update_task(id: str, data: dict):
    '''
    Return: 
            true, once the task element got updated.
            false, if an empty request body is sent.
    '''
    if len(data) < 1:
        return False
    task = await FASTAPI_collection.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = await FASTAPI_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task:
            return True
        return False



@app.post("/send-notification/{email}/{task_id}")
async def send_notification(email: str, task_id: str,background_tasks: BackgroundTasks, request: Request):
    '''
    Validate whether the task_id present in the database.
    If the task id is present, it'll send the mail to the given email address.
    '''
    
    client_email = str(email)
    tasks_id = []
    async for task in FASTAPI_collection.find():
        tasks_id.append(str(task["_id"]))

    if task_id in tasks_id:
        task_data = await FASTAPI_collection.find_one({"_id": ObjectId(task_id)})
        print(task_data)
        print(type(task_data))
        task = task_data['task_name'] 
        due = task_data['due_date']
        print(task,due)
        msg = "You have a task "+ task + " on due date " + due
        print(type(msg))
        write_notification(client_email, message=msg)
        logging.info("Notification sent in the background")
        return True
    return False
    