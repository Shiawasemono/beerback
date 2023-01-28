from typing import List, Dict

import uvicorn

from models import *

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import HTTPException, status

from dotenv import dotenv_values
from pymongo import MongoClient

import random

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    if __name__ == "__main__":
        app.mongodb_client = MongoClient("mongodb://localhost:27017/")
        app.database = app.mongodb_client["iSpindel_db"]
    else:
        app.mongodb_client = MongoClient(config["DB_URI"])
        app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/iSpindel/{id}", response_description="Get a single iSpindel by id", response_model=List[iSpindel])
def find_iSpindel(id: str):
    query = {"in_use": True}
    if (iSpindel_list := app.database[id].find(query)) is not None:
        return list(iSpindel_list)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"iSpindel with ID {id} not found")

@app.get("/iSpindels", response_description="Get all iSpindel names", response_model=Dict[str, Optional[iSpindelDB]])
def find_all_iSpindel():
    if (iSpindels := app.database.list_collection_names()) is not None:
        iSpindel_dict = {}
        for iSpindel in iSpindels:
            if (iSpindel == "active_devices"): continue
            iSpindel_dict[iSpindel] = list(app.database[iSpindel].find().sort("datetime", -1))[0]
        print(iSpindel_dict)
        return iSpindel_dict
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No iSpindels found")

@app.get("/activeDevices", response_description="Get all active devices", response_model=List[activateiSpindel])
def find_all_active():
    if len(active_devices :=  list(app.database["active_devices"].find({}))) > 0:
        return active_devices
    else:
        return []

@app.get("/historical/{name}/{date}", response_description="Get all active devices", response_model=List[iSpindelDB])
def find_all_active(name, date):
    iSpindel = app.database[name].find(
        {'datetime':{'$lte':datetime.now(), '$gt':datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")}}
    )
    return list(iSpindel)

@app.post("/iSpindel", response_description="Create a new iSpindel device or update an existing one", status_code=status.HTTP_202_ACCEPTED, response_model=iSpindelDB)
async def read_ispindel(iSpindel: iSpindel):
    iSpindel_dict = {k: v for k, v in iSpindel.dict().items() if v is not None}
    iSpindel_dict["_id"] = "".join(random.choice("0123456789ABCDEF") for _ in range(16))
    iSpindel_dict["datetime"] = datetime.now()
    new_iSpindel = app.database[iSpindel_dict["name"]].insert_one(iSpindel_dict)
    created_iSpindel = app.database[iSpindel_dict["name"]].find_one(
        {"_id": new_iSpindel.inserted_id}
    )
    return created_iSpindel

@app.post("/activateiSpindel", response_description="Activates iSpindel device", status_code=status.HTTP_202_ACCEPTED, response_model=List[activateiSpindel])
async def read_ispindel(req: activateiSpindelDB):
    if req.in_use:
        if len(list(app.database["active_devices"].find({"name": req.name}))) == 0 and req.name in app.database.list_collection_names():
            app.database["active_devices"].insert_one({"name": req.name, "time": req.time})
    else:
        if app.database["active_devices"].find({"name": req.name}) is not None and req.name in app.database.list_collection_names():
            app.database["active_devices"].delete_one({"name": req.name})
    return find_all_active()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)