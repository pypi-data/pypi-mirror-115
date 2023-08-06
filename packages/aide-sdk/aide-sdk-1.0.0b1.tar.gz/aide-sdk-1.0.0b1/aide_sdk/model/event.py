import copy
import dataclasses
from json import JSONDecodeError
from typing import List

import marshmallow.exceptions

from aide_sdk.logger.logger import LogManager
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.origin import Origin
from aide_sdk.model.resource import Resource
from aide_sdk.messaging.schemas.event import EventSchema
from aide_sdk.manifests.execution_context import ExecutionContext


@dataclasses.dataclass
class Event:
    correlation_id: str
    origin: Origin
    resources: List[Resource]
    executions: List[ExecutionContext]

    def add_resources(self, resources):
        self.resources.extend(resources)

    def add_execution(self, execution_context: ExecutionContext):
        self.executions.append(execution_context)

    def add_resources_from_context(self, context: OperatorContext):
        self.resources.extend(context._added_resources)

    def create_operator_context(self, execution_context: ExecutionContext):
        event_resources = [copy.deepcopy(x) for x in self.resources]
        origin = copy.deepcopy(self.origin)
        return OperatorContext(origin, event_resources, execution_context, self.correlation_id)

    def to_message(self):
        try:
            LogManager.get_audit_logger().debug("Serialising event")
            schema = EventSchema()
            message = schema.dumps(self)
            return message
        except Exception:
            LogManager.get_audit_logger().error("Could not serialise event")
            raise

    @classmethod
    def from_message(cls, message):
        try:
            schema = EventSchema()
            data = schema.loads(message)
            event = Event(**data)
            return event
        except (marshmallow.exceptions.MarshmallowError, JSONDecodeError):
            LogManager.get_audit_logger().error("Error deserialising input event")
            raise
        except Exception:
            LogManager.get_audit_logger().error("Could not load event data")
            raise
