from typing import Callable, List
from datetime import datetime
import math

from db_redis import get_value, set_value
from receipt import Receipt

ScoringFunctions = List[Callable[[Receipt], int]]

TIME_BASED_START = datetime.strptime("14:00", "%H:%M").time()
TIME_BASED_END = datetime.strptime("16:00", "%H:%M").time()


def calculate_retailer_points(receipt: Receipt) -> int:
    """Calculate points based on alphanumeric characters in the retailer name."""
    return sum(map(str.isalnum, receipt.retailer))


def calculate_round_total_points(receipt: Receipt) -> int:
    """Award 50 points if the total is a whole number."""
    return 50 if receipt.total.is_integer() else 0


def calculate_multiple_of_25_points(receipt: Receipt) -> int:
    """Award 25 points if the total is a multiple of 0.25."""
    return 25 if receipt.total % 0.25 == 0 else 0


def calculate_item_pair_points(receipt: Receipt) -> int:
    """Award 5 points for every pair of items."""
    return (len(receipt.items) // 2) * 5


def calculate_description_points(receipt: Receipt) -> int:
    """
    Award points based on item descriptions if length is divisible by 3.  
    Multiply the price by 0.2 and round up to the nearest integer.
    """
    return sum(
        map(
            lambda item: math.ceil(item.price * 0.2)
            if len(item.shortDescription.strip()) % 3 == 0
            else 0,
            receipt.items,
        )
    )


def calculate_odd_day_points(receipt: Receipt) -> int:
    """Award 6 points if the purchase date is an odd day."""
    return 6 if datetime.strptime(receipt.purchaseDate, "%Y-%m-%d").day % 2 == 1 else 0


def calculate_time_based_points(receipt: Receipt) -> int:
    """Award 10 points if the purchase time is between TIME_BASED_START and TIME_BASED_END."""
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M").time()
    return 10 if TIME_BASED_START < purchase_time < TIME_BASED_END else 0


DEFAULT_SCORING_FUNCTIONS: ScoringFunctions = [
    calculate_retailer_points,
    calculate_round_total_points,
    calculate_multiple_of_25_points,
    calculate_item_pair_points,
    calculate_description_points,
    calculate_odd_day_points,
    calculate_time_based_points,
]


def calculate_total_points(
    receipt: Receipt, scoring_functions: ScoringFunctions = None
) -> int:
    """Calculate total points by applying all scoring functions."""
    return sum(
        map(lambda fn: fn(receipt), scoring_functions)
    )


def save_points(receipt_id: str, points: int) -> None:
    """Store points into data layer."""
    set_value(f"points:{receipt_id}", points, expiry=3600)


def get_points(receipt_id: str) -> int:
    """Retrieve points from data layer."""
    return get_value(f"points:{receipt_id}") or 0
