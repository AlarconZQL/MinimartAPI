from flask_restx import Namespace, Resource
from app.services.voucher import VoucherService
from app.schemas.voucher import VoucherSchema
from flask import Response

api = Namespace('voucher', description='Voucher\'s operations')


@api.route('/')
class Voucher(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Retrieve all existing vouchers"""
        vouchers = VoucherService.get_all_vouchers()
        voucher_schema = VoucherSchema(many=True)
        result = voucher_schema.dump(vouchers)
        return result, 200
