import pytest
from opentelemetry import trace
from opentelemetry.baggage import get_all, set_baggage, set_value
from opentelemetry.context import attach
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from fan_tools.otel.helpers import extract_span, get_tracer, inject
from fan_tools.otel.jaeger_tracing import setup_jaeger_tracer


@pytest.fixture(autouse=True)
def prepare():
    provider = TracerProvider()
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def test_01_simple_pass():

    # create context
    # set baggage
    # inject
    # extract into new clear context
    # check baggage
    tracer = get_tracer('example')
    headers = {}
    with extract_span({}, 'inner', 'name'):
        ctx1 = set_baggage('example-b', 'value')
        ctx2 = set_baggage('example-boooooooooooooooooooo', 'valueoooooooooooooooooo', context=ctx1)
        attach(ctx2)
        # assert False, dict(get_all())
        inject(headers)
    h1 = {}
    inject(h1)
    # assert False, h1
    # assert False, headers

