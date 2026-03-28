from .base import BaseAPIException

#Cart
class EmptyCartException(BaseAPIException):
    status_code = 400
    default_detail = 'Cart is empty'
    error_code = 'empty_cart'

class InvalidQuantityException(BaseAPIException):
    status_code = 400
    default_detail = 'Quantity must be greater than 0'
    error_code = "invalid_quantity"

#Stock -  Product
class OutOfStockException(BaseAPIException):
    status_code = 400
    default_detail = 'Not enough stock'
    error_code = 'out_of_stock'

class ProductInactiveException(BaseAPIException):
    status_code = 400
    default_detail = 'Product is inactive'
    error_code = 'product_inactive'

#Order - Payment
class AlreadyPaidException(BaseAPIException):
    status_code = 400
    default_detail = 'Order already paid'
    error_code = "already_paid"

class OrderNotReadyException(BaseAPIException):
    status_code = 400
    default_detail = 'Order not ready for payment'
    error_code = 'order_not_ready'