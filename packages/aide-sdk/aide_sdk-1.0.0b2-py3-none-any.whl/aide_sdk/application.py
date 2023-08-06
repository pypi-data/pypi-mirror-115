from aide_sdk.inference.inference_manager import InferenceManager
from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.manifests.manifest import load
from aide_sdk.messaging.config import QueueConfiguration
from aide_sdk.messaging.consumer import ModelConsumer
from aide_sdk.messaging.publisher import ModelPublisher


class ModelFailure(Exception):
    pass


class AideApplication:
    @staticmethod
    def start(operator: AideOperator) -> None:
        manifest = load()
        consumer_config = QueueConfiguration(queue=manifest.get_queue_name())
        publisher_config = QueueConfiguration(queue="output")

        model_consumer = ModelConsumer(consumer_config)
        model_publisher = ModelPublisher(publisher_config)

        manager = InferenceManager(model_consumer, model_publisher, operator)
        manager.execute()
