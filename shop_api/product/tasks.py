from celery import shared_task
from time import sleep
from shop_api.celery import app
from datetime import datetime

@app.task()
def download():
    print("START")
    sleep(15)
    print("END")
    return "OK"

@shared_task
def log_new_product(product_id, product_title):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"[{now}] Новый продукт создан!")
    print(f"ID: {product_id}")
    print(f"Название: {product_title}")
    print("-" * 40)
    
    return f"Продукт {product_title} залогирован"