from app.models.voucher import Voucher


class VoucherService:
    @classmethod
    def get_voucher(cls, voucher_id):
        """Retrieves a single product"""
        return Voucher.query.get(voucher_id)
