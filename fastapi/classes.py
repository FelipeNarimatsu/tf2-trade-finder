from pydantic import BaseModel

class Request_Trade(BaseModel):
    id:         int
    item_name:  str
    sell_price: float
    buy_price:  float
    profit:     float
