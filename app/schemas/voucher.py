from app import ma
from app.models import Voucher


class VoucherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Voucher
        ordered = True

    id = ma.auto_field()
    code = ma.auto_field()
    store_id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
