import models
import yfinance
from fastapi import FastAPI, Request, Depends, BackgroundTasks, Response
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session

from models import Stock, StockRequest

# the app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    adding tickers to database
    """

    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    #background_tasks.add_task(, stock.id)  # TODO

    return Response(status_code=201)