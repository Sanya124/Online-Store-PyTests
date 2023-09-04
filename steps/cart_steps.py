import uuid


class CartSteps:

    @staticmethod
    def add_item(item_id: str = None, shopping_session_id: str = None) -> dict:
        """Data for adding item in cart to be sent via the REST API"""
        data = {
            'shoppingSessionId': shopping_session_id if shopping_session_id else str(uuid.uuid4()),
            'itemId': item_id if item_id else str(uuid.uuid4())
        }
        return data
