from fastapi import FastAPI
from routes.reserverout import router as resrouter
from routes.tableroute import router as tablerouter


app = FastAPI()
app.include_router(resrouter)
app.include_router(tablerouter)