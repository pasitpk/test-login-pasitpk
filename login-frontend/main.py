import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_REDIRECT_URI = str(os.getenv("LINE_REDIRECT_URI"))
LINE_CHANNEL_ID = str(os.getenv("LINE_CHANNEL_ID"))
LINE_CHANNEL_SECRET = str(os.getenv("LINE_CHANNEL_SECRET"))

app = FastAPI()


@app.get("/verify-line-token/")
async def verify_line_token(request: Request):
    
    q_params = dict(request.query_params)
    for k, v in q_params.items():
        print(f'{k}: {v}')
    
    token_info = await get_access_token(q_params['code'], LINE_REDIRECT_URI, LINE_CHANNEL_ID, LINE_CHANNEL_SECRET)
    for k, v in token_info.items():
        print(f'{k}: {v}')

    user_info = await verify_id_token(token_info['id_token'], LINE_CHANNEL_ID)
    for k, v in user_info.items():
        print(f'{k}: {v}')

    return q_params, token_info, user_info
  

async def get_access_token(code, redirect_uri, client_id, client_secret):
    endpoint = 'https://api.line.me/oauth2/v2.1/token'
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    res = requests.post(endpoint, data=payload, headers=headers)
    data = res.json()

    return data


async def verify_id_token(id_token, client_id):
    endpoint = 'https://api.line.me/oauth2/v2.1/verify'
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'id_token': id_token,
        'client_id': client_id,
    }
    res = requests.post(endpoint, data=payload, headers=headers)
    data = res.json()

    return data


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