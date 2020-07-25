class NoStockException(Exception):
    def __init__(self, message='There is no stock of this product at this store'):
        self.message = message


class ProductNotFoundInCart(Exception):
    def __init__(self, message='This cart does not have any unit of this product'):
        self.message = message


class VoucherNotValidException(Exception):
    def __init__(self, message='This voucher is not valid'):
        self.message = message
