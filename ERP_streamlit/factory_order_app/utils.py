import datetime
from i18n import ORDER_CLASSES

def generate_order_number(order_class_index: int, material_type: str):
    now = datetime.datetime.now()
    prefix = "MO"
    order_class: str = ORDER_CLASSES["en"][order_class_index]
    return f"{prefix}-{order_class[:1]}{material_type}-{now.strftime('%Y%m%d%H%M%S')}"