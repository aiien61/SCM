from enum import Enum
from typing import Dict, List

class Status(Enum):
    PENDING = 'Pending'
    PROCESSED = 'Processed'
    SHIPPED = 'Shipped'

class TrackableMixin:
    def __init__(self, *args, **kwargs):
        self.tracking_info: Dict[str, str] = {}
        super().__init__(*args, **kwargs)

    def update_tracking(self, info: Dict[str, str]) -> None:
        self.tracking_info.update(info)
    
    def get_tracking_info(self) -> Dict[str, str]:
        return self.tracking_info
    

class NotifiableMixin:
    def __init__(self, *args, **kwargs):
        self.notifications: List[str] = []
        super().__init__(*args, **kwargs)
    
    def add_notification(self, message: str) -> None:
        self.notifications.append(message)

    def get_notifications(self) -> List[str]:
        return self.notifications
    
class Order(TrackableMixin, NotifiableMixin):
    def __init__(self, order_id: int, items: List[str]):
        self.order_id = order_id
        self.items = items
        self.status = Status.PENDING
        super().__init__()

    def process_order(self) -> None:
        # Process the order
        self.status = Status.PROCESSED
        self.add_notification(f"Order {self.order_id} has been processed.")
        self.update_tracking({'status': self.status.value})
    
class Shipment(TrackableMixin, NotifiableMixin):
    def __init__(self, shipment_id: int, destination: str):
        self.shipment_id = shipment_id
        self.destination = destination
        self.status = Status.PENDING
        super().__init__()

    def ship(self) -> None:
        # Ship the items
        self.status = Status.SHIPPED
        self.add_notification(f"Shipment {self.shipment_id} has been shipped.")
        self.update_tracking({'status': self.status.value})

# Example usage
order = Order(order_id=1001, items=['item1', 'item2'])
order.process_order()
print(order.get_notifications())  # Output: ['Order 1001 has been processed.']
print(order.get_tracking_info())  # Output: {'status': 'processed'}

shipment = Shipment(shipment_id=1100, destination='Warehouse A')
shipment.ship()
print(shipment.get_notifications())  # Output: ['Shipment 1100 has been shipped.']
print(shipment.get_tracking_info())  # Output: {'status': 'shipped'}
