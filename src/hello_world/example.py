import json
import boto3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.trace import SpanKind, Link, format_span_id, format_trace_id, NonRecordingSpan, SpanContext

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)


def lambda_handler(event, context):
    with tracer.start_as_current_span("parent_span") as span:
        span_context: SpanContext = span.get_span_context()
        otel_context = trace.set_span_in_context(NonRecordingSpan(span_context))

        print("Hello World")
        with tracer.start_as_current_span("child_span", context=otel_context):
            print("Hello World from Child Span")

        # This will issue an STS call, which should be filtered out
        sts_client = boto3.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]
        print(f"Account ID: {account_id}")

        # This will list all S3 buckets in the account, which should be filtered out
        s3_client = boto3.client("s3")
        response = s3_client.list_buckets()
        print("S3 Buckets:", response["Buckets"])

        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
