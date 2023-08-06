from json import JSONDecodeError

from marshmallow.exceptions import MarshmallowError

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.logger.logger import LogManager
from aide_sdk.manifests.execution_context import start_new_execution
from aide_sdk.messaging.consumer import ModelConsumer
from aide_sdk.messaging.publisher import ModelPublisher
from aide_sdk.model.event import Event

logger_audit = LogManager.get_audit_logger()


class InferenceManager:
    def __init__(self, consumer: ModelConsumer, publisher: ModelPublisher, operator: AideOperator):
        self.operator = operator
        self.consumer = consumer
        self.publisher = publisher

    def execute(self):
        """Starts the model consumer and the model publisher brokers"""
        self.consumer.set_callback(self.on_input_received)
        self.consumer.start()
        self.publisher.start()

    def on_input_received(self, message: str):
        """Callback that is called when a new input is consumed from the
        operator's input queue
        :param message: a json message
        """
        execution_context = start_new_execution()

        try:
            event = Event.from_message(message)
            operator_context = event.create_operator_context(execution_context)

            # Execute operator
            result_context = self._execute_process(operator_context, event)

            # Gather new resources
            event.add_resources_from_context(result_context)

            # Log this execution
            event.add_execution(execution_context)

            # Publish new event back to input queue
            self._execute_publish(event)
        except (MarshmallowError, JSONDecodeError):
            logger_audit.exception("Model input message could not be parsed")
        except Exception:
            logger_audit.exception("Model has encountered an error")

    def _execute_process(self, operator_context, event):
        logger_audit.info("Model prediction started",
                          extra={"props": {"correlation_id": event.correlation_id}})
        result = self.operator.process(operator_context)
        logger_audit.info("Model prediction finished",
                          extra={"props": {"correlation_id": event.correlation_id}})
        return result

    def _execute_publish(self, event):
        logger_audit.info("Publishing model output started",
                          extra={"props": {"correlation_id": event.correlation_id}})
        self.publisher.publish_message(event.to_message(), event.correlation_id)
        logger_audit.info("Publishing model output finished",
                          extra={"props": {"correlation_id": event.correlation_id}})
