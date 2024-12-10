from fastapi import FastAPI
from pydantic import BaseModel
from Bs4SearchList import list_data
from Bs4DetailInfo import detail_data
app = FastAPI() # FastAPI 인스턴스 앱 생성

# async def get_list():
