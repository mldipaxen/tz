from fastapi import FastAPI
from reserverout import router as resrouter
from tableroute import router as tablerouter
import uvicorn 


app = FastAPI()
app.include_router(resrouter)
app.include_router(tablerouter)

