import pytest
import requests

BASE_URL = "http://app:8080"

def submit_receipt(data):
    """Helper function to send a POST request."""
    url = f"{BASE_URL}/receipts/process"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()

def get_points(receipt_id: str):
    """Helper function to send a GET request."""
    response = requests.get(f"{BASE_URL}/receipts/{receipt_id}/points")
    response.raise_for_status()

    return response.json()

@pytest.mark.parametrize(
    "receipt_data, expected",
    [
        (
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            },
            109,
        ),
        (
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            },
            28,
        ),
    ],
)
def test_receipt_calculation(receipt_data, expected):
    submit_response = submit_receipt(receipt_data)
    assert submit_response

    receipt_id = submit_response["id"]
    assert receipt_id

    points_response = get_points(receipt_id)
    assert points_response

    assert points_response["points"] == expected
