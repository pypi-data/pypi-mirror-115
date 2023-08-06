import os


class QueueConfiguration:
    def __init__(self, username="", password="", host="", port="", model_exchange="", output_exchange="", model_routing_key="", output_routing_key="", queue=""):
        self.username = username if username != "" else os.getenv("RABBITMQ_USERNAME", "admin")
        self.password = password if password != "" else os.getenv("RABBITMQ_PASSWORD", "admin")
        self.host = host if host != "" else os.getenv("RABBITMQ_HOST", "localhost")
        self.port = port if port != "" else os.getenv("RABBITMQ_PORT", 5672)
        self.model_exchange = model_exchange if model_exchange != "" else os.getenv("RABBITMQ_MODEL_EXCHANGE", "model-exchange")
        self.output_exchange = output_exchange if output_exchange != "" else os.getenv("RABBITMQ_OUTPUT_EXCHANGE", "output-exchange")
        self.model_routing_key = model_routing_key if model_routing_key != "" else os.getenv("RABBITMQ_MODEL_ROUTING_KEY", "")
        self.output_routing_key = output_routing_key if output_routing_key != "" else os.getenv("RABBITMQ_OUTPUT_ROUTING_KEY", "output")
        self.queue = queue
