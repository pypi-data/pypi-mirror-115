from marshmallow import Schema, fields, post_load

from aide_sdk.manifests.execution_context import ExecutionContext


class ExecutionSchema(Schema):
    model_uid = fields.Str()
    execution_uid = fields.UUID()

    @post_load
    def make_object(self, data, **kwargs):
        return ExecutionContext(**data)
