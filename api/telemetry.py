from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.datadog import DatadogSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app):
    trace.set_tracer_provider(TracerProvider())
    exporter = DatadogSpanExporter(agent_url="http://datadog-agent.default.svc.cluster.local:8126", service="pollutrack-api")
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
