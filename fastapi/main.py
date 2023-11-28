from fastapi import FastAPI, HTTPException
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

@app.delete("/delete_trades_id/{trade_id}")
def delete_trade_id(trade_id: int):
    trades = session.get(Trades, trade_id)
    if not trades:
        raise HTTPException(status_code=404, detail="Trade not found!")
    session.delete(trades)
    session.commit()
    return {"status": "Delete success",
            "data": trades}