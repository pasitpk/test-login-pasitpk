import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import requests
import boto3
import random
from dotenv import load_dotenv

load_dotenv()

LINE_REDIRECT_URI = str(os.getenv("LINE_REDIRECT_URI"))
LINE_CHANNEL_ID = str(os.getenv("LINE_CHANNEL_ID"))
LINE_CHANNEL_SECRET = str(os.getenv("LINE_CHANNEL_SECRET"))
AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
AWS_REGION_NAME = str(os.getenv("AWS_REGION_NAME"))

app = FastAPI()


@app.post("/send-otp/")
async def send_otp(request: Request):
    
    data = await request.json()

    client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
    )

    phone_number = data['phone_number']
    otp = str(random.randint(0, 999999)).zfill(6)
    client.publish(
    PhoneNumber=phone_number,
    Message=f"{otp} is your OTP for CCCNLab's application"
    )

    return phone_number, otp


if __name__ == "__main__":
    
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    ssl_keyfile = os.getenv("SSL_KEYFILE")
    ssl_certfile = os.getenv("SSL_CERTFILE")
    ssl_keyfile_password = os.getenv("SSL_KEYFILE_PASSWORD")

    if host.startswith('http://'):
        host = host[7:]
    elif host.startswith('https://'):
        host = host[8:]
        
    uvicorn.run(app, 
                host=host, 
                port=int(port), 
                ssl_keyfile=ssl_keyfile if ssl_keyfile else None, 
                ssl_certfile=ssl_certfile if ssl_certfile else None,
                ssl_keyfile_password=ssl_keyfile_password if ssl_keyfile_password else None,
                )
