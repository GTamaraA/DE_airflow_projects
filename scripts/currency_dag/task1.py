import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base
import os


load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


DB_URL = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
print(DB_URL)
XML_PATH = 'https://www.cbr.ru/scripts/XML_valFull.asp'

engine = create_engine(url=DB_URL, echo=True)
#Модели не создаем, т.к. пандас сам создает таблицу
#Base.metadata.create_all(bind=engine, checkfirst=True)

SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)
sessionlocal = SessionLocal()

df = pd.read_xml(XML_PATH, encoding='windows-1251')
df.to_sql(
    name='val_dict',
    con=engine,
    if_exists='delete_rows',
    index=False
)

print('Справочник загружен')