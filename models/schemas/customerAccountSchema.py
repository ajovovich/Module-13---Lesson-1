from marshmallow import fields
from schema import ma

class CustomerAccount(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    roles = fields.List(fields.String, required=True)

class Meta:
    fields = ("id", "username", "password", "customer_id", "roles")

customer_account_schema = CustomerAccount()
customer_accounts_schema = CustomerAccount(many=True)