from fastapi import FastAPI,Header,Depends,HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database import urls
from pymongo import MongoClient
from qrcode import qr_code

connection_string = "mongodb+srv://cosdp:kdp1234@mflix.slvq0y2.mongodb.net/test"
mongo_db = MongoClient(connection_string)
databsae = mongo_db.UrlShortner
collection = databsae.urls

qr_obj = qr_code()
base_url = "http://127.0.0.1:8000/"
url_obj = urls(collection)
class addURL(BaseModel):
    special_key : str
    url : str

app = FastAPI()

@app.get("/")# http://127.0.0.1:8000/9ai
async def hello():
    return "HELLO FAST API WORLD"

@app.get("/{specialKey}")# http://127.0.0.1:8000/hi
async def new(specialKey:str):
    url = url_obj.fetch_url(specialKey)
    return RedirectResponse(url,status_code=302)

@app.post("/addURL")
async def addurl(json:addURL):
    insert = url_obj.insert_url(json.special_key,json.url)
    if insert:
        return {"Shortened URL":base_url+json.special_key}
    return {"Shortening of URL":insert}

@app.get("/count/{specialkey}")
async def count_clicks(specialkey:str):
    return url_obj.count(specialkey)

@app.get("/qrcode/{specialkey}")
async def make_qr(specialkey:str):
    qr_obj.make_qr(base_url+specialkey,specialkey)
    return FileResponse(specialkey+".png")