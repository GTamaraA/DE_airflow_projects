import logging
from dotenv import load_dotenv
import os
import argparse
from zeep import Client
import datetime as dt
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, valsFull

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Загрузка даты (за какой день загружаем данные)
logging.info('Обработка входящей даты...')

parser = argparse.ArgumentParser()
parser.add_argument('--date')
args = parser.parse_args()
load_date = dt.datetime.strptime(args.date, '%Y-%m-%d')

logging.info(f'Обработка данных за {load_date}...')

DB_URL = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

def db_init():
    logging.info('Инициализация БД...')
    
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)

    return engine

def extract_n_load_valsFull(engine, logicaldate):
    # Создание подключения
    sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    postgres_session = sessionLocal()

    # Настройка выгрузки данных
    wsdl = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'

    client = Client(wsdl)

    logging.info('Выгрузка данных...')
    with client.settings(raw_response=True):
        response = client.service.GetCursOnDate(On_date=logicaldate)

    soup = BeautifulSoup(response.content, 'xml')

    data = []
    for item in soup.find_all('ValuteCursOnDate'):
        row = {
            'vname':     str(item.find('Vname').string).strip(),
            'vnom':      item.find('Vnom').string,
            'vcurs':     item.find('Vcurs').string,
            'vcode':     item.find('Vcode').string,
            'vchcode':   item.find('VchCode').string,
            'vunitrate': item.find('VunitRate').string,
            'ondate':    logicaldate
        }
        data.append(row)

    logging.info('Загрузка данных в БД...')
    postgres_session.bulk_insert_mappings(valsFull, data)
    postgres_session.commit()
    postgres_session.close()
    logging.info('Загрузка данных в БД выполнена! ✅')

engine = db_init()
extract_n_load_valsFull(engine=engine, logicaldate=load_date)
