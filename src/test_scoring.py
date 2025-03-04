import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from scoring import calculate_total_points, DEFAULT_SCORING_FUNCTIONS
from receipt import Receipt


def generate_item():
    return st.fixed_dictionaries(
        {
            "shortDescription": st.text(min_size=1, max_size=50),
            "price": st.decimals(min_value=0.01, max_value=1000, places=2).map(
                lambda x: f"{x:.2f}"
            ),
        }
    )


@given(
    retailer=st.text(min_size=1, max_size=50),
    purchase_date=st.dates(
        min_value=datetime(2000, 1, 1).date(), max_value=datetime(2100, 12, 31).date()
    ).map(lambda d: d.strftime("%Y-%m-%d")),
    purchase_time=st.times().map(lambda t: t.strftime("%H:%M")),
    items=st.lists(generate_item(), min_size=0, max_size=20),
    total=st.decimals(min_value=0.01, max_value=10000, places=2).map(
        lambda x: f"{x:.2f}"
    ),
)
def test_default_calculate_points(retailer, purchase_date, purchase_time, items, total):
    receipt_data = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "items": items,
        "total": total,
    }
    receipt = Receipt(**receipt_data)
    points = calculate_total_points(
        receipt, scoring_functions=DEFAULT_SCORING_FUNCTIONS
    )

    # Basic property tests
    assert isinstance(points, int), "Points should be an integer"
    assert points >= 0, "Points should never be negative"

    # Additional invariants
    if float(total).is_integer():
        assert points >= 50, "Should get at least 50 points for a round total"
    if float(total) % 0.25 == 0:
        assert points >= 25, "Should get at least 25 points for total multiple of 0.25"
    if len(items) >= 2:
        assert (
            points >= (len(items) // 2) * 5
        ), "Should get at least 5 points for every two items"

    odd_day = int(purchase_date.split("-")[-1]) % 2 == 1
    if odd_day:
        assert points >= 6, "Should get 6 points for an odd day"

    purchase_hour = int(purchase_time.split(":")[0])
    if 14 <= purchase_hour < 16:
        assert (
            points >= 10
        ), "Should get 10 points for purchases between 2:00pm and 4:00pm"


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
    receipt = Receipt(**receipt_data)
    points = calculate_total_points(
        receipt, scoring_functions=DEFAULT_SCORING_FUNCTIONS
    )
    assert points == expected
