# main_router.py
from fastapi import APIRouter

main_router = APIRouter()

@main_router.get('/')
def home():
    return 'This is 10 Academy promptly API'
