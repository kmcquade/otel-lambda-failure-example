import json
import boto3
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
        # This will issue an STS call, which should be filtered out
        sts_client = boto3.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]
        print("Account ID:", account_id)

        # This will list all S3 buckets in the account, which should be filtered out
        s3_client = boto3.client("s3")
        response = s3_client.list_buckets()
        print("S3 Buckets:", response["Buckets"])

        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
