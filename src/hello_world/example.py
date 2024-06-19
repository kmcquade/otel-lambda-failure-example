import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)


def lambda_handler(event, context):
    with tracer.start_as_current_span("example_span"):
        print("Hello World")
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
