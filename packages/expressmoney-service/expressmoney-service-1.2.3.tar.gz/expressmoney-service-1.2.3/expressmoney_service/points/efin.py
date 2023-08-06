__all__ = ('EfinILOrderPoint', 'EfinCancelOrderPoint')

from ..api import *
from phonenumber_field.serializerfields import PhoneNumberField

_SERVICE = 'services'


class _EfinILOrderCreateContract(Contract):
    product_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    city = serializers.CharField(max_length=32)
    address = serializers.CharField(max_length=250)
    phonenumber = PhoneNumberField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    meeting_day = serializers.DateField()


class _EfinILOrderReadContract(Contract):
    created = serializers.DateTimeField()
    meeting_day = serializers.DateField()
    sign_day = serializers.DateField()
    status_code = serializers.IntegerField()
    status_name = serializers.CharField(max_length=150)
    status_description = serializers.CharField(max_length=256)
    status_date = serializers.DateTimeField(allow_null=True)


class _EfinCancelOrderCreateContract(Contract):
    pass


class _EfinILOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'efin_il_order'


class _EfinCancelOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'set_canceled'


class EfinILOrderPoint(CreatePointMixin, ListPointMixin, ContractPoint):
    _point_id = _EfinILOrder()
    _create_contract = _EfinILOrderCreateContract
    _read_contract = _EfinILOrderReadContract
    _sort_by = 'created'


class EfinCancelOrderPoint(CreatePointMixin, ContractPoint):
    _point_id = _EfinCancelOrder()
    _create_contract = _EfinCancelOrderCreateContract
