from fastapi import FastAPI
from classes import Request_Trade
from models import Trades, session
import os

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "SUCCESS",
        "data": "NO DATA"
    }

@app.get("/trades")
async def get_all_trades():
    trades_query = session.query(Trades)
    trades = trades_query.all()
    return {
        "status": "SUCCESS",
        "data": trades
    }