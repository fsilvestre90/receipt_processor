import logging
from celery_worker import celery_app
from scoring import calculate_total_points, save_points, DEFAULT_SCORING_FUNCTIONS
from receipt import Receipt

logger = logging.getLogger("")

@celery_app.task(
    ignore_result=False,
    bind=True,
)
def calculate_points(self, receipt, receipt_id):
    serialized_receipt = Receipt.model_validate_json(receipt)
    points = calculate_total_points(
        receipt=serialized_receipt, 
        scoring_functions=DEFAULT_SCORING_FUNCTIONS
    )
    logger.info(f"Calculated points={points}")
    save_points(
        receipt_id=receipt_id, 
        points=points
    )
    return points
