import uuid

from fastapi import FastAPI

from tasks import calculate_points
from scoring import get_points
from receipt import Receipt

app = FastAPI()


@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    calculate_points.delay(receipt.model_dump_json(), receipt_id)
    return {"id": receipt_id}


@app.get("/receipts/{id}/points")
def get_receipt_points(id: str):
    points = get_points(id)
    return {"points": points}
