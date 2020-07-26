from app.models.voucher import Voucher


class VoucherService:
    @classmethod
    def get_voucher(cls, voucher_id):
        """Retrieves a single voucher"""
        return Voucher.query.get(voucher_id)

    @classmethod
    def get_all_vouchers(cls):
        """Retrieves all existing vouchers """
        return Voucher.query.all()
