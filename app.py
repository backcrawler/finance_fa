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


@app.get("/")
async def home(request: Request, dividend=None, ma50=None, ma200=None, db: Session = Depends(get_db)):
    """show all stocks"""
    stocks = db.query(Stock)
    if dividend:
        stocks = stocks.filter(Stock.dividend_yield > dividend)
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)
    stocks = stocks.all()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "stocks": stocks,
        "dividend": dividend,
        "ma200": ma200,
        "ma50": ma50
    })


def get_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    yahoo_data = yfinance.Ticker(stock.symbol)
    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.dividend = yahoo_data.info['dividendYield'] * 100
    db.add(stock)
    db.commit()


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """adding tickers to database"""
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    background_tasks.add_task(get_stock_data, stock.id)
    return Response(status_code=201)