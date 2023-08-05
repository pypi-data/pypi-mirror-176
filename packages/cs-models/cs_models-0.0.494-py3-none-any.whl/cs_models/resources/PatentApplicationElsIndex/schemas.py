from marshmallow import (
    Schema,
    fields,
    validate,
)


class PatentApplicationElsIndexResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    patent_application_id = fields.Integer(required=True)
    els_indexed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
