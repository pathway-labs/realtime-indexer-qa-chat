from __future__ import annotations

import logging
import os
import sys

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import (
    SERVICE_INSTANCE_ID,
    SERVICE_NAME,
    SERVICE_VERSION,
    Resource,
)

PATHWAY_TELEMETRY_ENDPOINT = os.environ.get("PATHWAY_TELEMETRY_SERVER")
APP_NAME = os.environ.get("APP_NAME")
PATHWAY_SERVICE_INSTANCE_ID = os.environ.get("PATHWAY_SERVICE_INSTANCE_ID")

logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)

resource = Resource(
    attributes={
        SERVICE_NAME: APP_NAME,
        SERVICE_VERSION: "",
        SERVICE_INSTANCE_ID: PATHWAY_SERVICE_INSTANCE_ID,
        "python.version": sys.version,
        "otel.scope.name": "python",
    }
)


def init_pw_log_config():
    if PATHWAY_TELEMETRY_ENDPOINT is not None:
        exporter = OTLPLogExporter(endpoint=PATHWAY_TELEMETRY_ENDPOINT)
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        set_logger_provider(logger_provider)
        logging.getLogger().addHandler(handler)
