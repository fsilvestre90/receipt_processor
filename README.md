# FastAPI-Celery-Redis-Flower  

## 🚀 Overview  

This project integrates **FastAPI** for API development, **Celery** for distributed task processing, and **Redis** as a message broker and storage 

## 🛠 Built With  
- [FastAPI](https://fastapi.tiangolo.com/) – Modern, high-performance web framework  
- [Celery](https://docs.celeryq.dev/en/stable/index.html#) – Distributed task queue  
- [Redis](https://redis.io/) – In-memory data store & message broker  

## 🔧 Setup & Usage  

**Build & Start** all services:  
   ```bash
      docker-compose up --build
   ```

**Submit receipt** curl request
```bash
curl -X POST "http://localhost:8080/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
         "retailer": "Target",
         "purchaseDate": "2022-01-01",
         "purchaseTime": "13:01",
         "items": [
             {
                 "shortDescription": "Mountain Dew 12PK",
                 "price": "6.49"
             },
             {
                 "shortDescription": "Emils Cheese Pizza",
                 "price": "12.25"
             },
             {
                 "shortDescription": "Knorr Creamy Chicken",
                 "price": "1.26"
             },
             {
                 "shortDescription": "Doritos Nacho Cheese",
                 "price": "3.35"
             },
             {
                 "shortDescription": "Klarbrunn 12-PK 12 FL OZ",
                 "price": "12.00"
             }
         ],
         "total": "35.35"
     }'
```

**Check points** curl request
```bash
curl -X GET "http://localhost:8080/receipts/86d3879e-b6bc-464e-951d-9320f7721912/points" \
     -H "Accept: application/json"
```