import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

from starlette.concurrency import run_in_threadpool
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
print(os.listdir(os.getcwd()))
templates = Jinja2Templates(directory='login-templates')
app = FastAPI()
app.mount("/static", StaticFiles(directory='login-templates'), name="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get("/verify-line-token")
async def verify_line_token(data):
    q_params = dict(req.query_params)
    for k, v in q_params:
        print(f'{k}: {v}')
    
if __name__ == "__main__":

    load_dotenv()
    
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