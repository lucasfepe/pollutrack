from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

resource = Resource.create({
    ResourceAttributes.SERVICE_NAME: "pollutrack-api",
    ResourceAttributes.SERVICE_VERSION: "1.0",
    ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development",
})

app = FastAPI()

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://datadog-agent:4318/v1/traces",
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

FastAPIInstrumentor.instrument_app(app)

@app.get("/api/v1/airquality")
async def read_data():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("read_airquality_data") as span:
        span.set_attribute("endpoint", "/api/v1/airquality")
        return {"status": "OK"}
