from app.models.voucher import Voucher


class VoucherService:
    @classmethod
    def get_voucher(cls, voucher_id):
        return Voucher.query.get(voucher_id)
