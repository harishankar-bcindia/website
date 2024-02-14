from fastapi import FastAPI, Request, Depends,HTTPException
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import threading
import time
import json
import pandas as pd
from enum import Enum
from fastapi import FastAPI,Request,Depends,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Harry Verifier 🔐",
    description='Made with ❤️ by Hari in India',
    summary="Authorizer",
    version="6.9.0",
    terms_of_service="https://getkloo.com/terms-conditions",
    contact={
        "name": "Harry Support",
        "url": "https://vashishthahari.weebly.com/",
        "email": "vashishthaharishankar@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    redoc_url=None,
    redirect_slashes=True
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

templates = Jinja2Templates(directory="templates")



class Dashboard(str,Enum):
    login = "login"
    signup = "signup"

@app.get("/home/")
async def main(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home/signup")
async def signup(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/home/signup/otp/", response_class=HTMLResponse)
async def otp(request: Request, first_name: str = Form(...), last_name: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    #form_data = await request.form()
    form_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    form_data_json = json.dumps(dict(form_data))
    print(form_data_json)
    #return HTMLResponse(content=json.dumps({"message": "Received form data", "form_data": form_data_json}))
    return templates.TemplateResponse("otp.html", {"request": request})

@app.get("/home/login")
async def login(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home/profile")
async def profile(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("profile.html", {"request": request})