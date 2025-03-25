import logging
import os
import uuid
import contextvars
from datetime import datetime, timezone
from pythonjsonlogger.json import JsonFormatter

# A context variable to store a mapping from service names to request IDs.
service_request_ids = contextvars.ContextVar("service_request_ids", default={})

class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        # Call the base implementation.
        super().add_fields(log_record, record, message_dict)
        
        # Format timestamp as ISO 8601 in UTC.
        log_record['timestamp'] = (
            datetime.fromtimestamp(record.created, tz=timezone.utc)
            .isoformat(timespec='milliseconds')
            .replace('+00:00', 'Z')
        )
        
        # Set log level.
        log_record['level'] = record.levelname
        
        # Ensure the service name is set.
        log_record.setdefault('service', getattr(record, 'service', 'unknown-service'))
        
        # If no requestId is provided, generate one (this is a fallback).
        if not log_record.get('requestId'):
            log_record['requestId'] = str(uuid.uuid4())
        
        # Ensure metadata and userId are available.
        log_record.setdefault('metadata', {})
        log_record.setdefault('userId', None)
        
        return log_record

class Logger:
    def __init__(self, service_name):
        self.service_name = service_name
        
        # Retrieve the current context's dictionary of request IDs.
        current_ids = service_request_ids.get()
        if service_name in current_ids:
            # Reuse the existing request ID for this service in this connection.
            self.requestId = current_ids[service_name]
        else:
            # Create a new request ID and store it in the context.
            self.requestId = str(uuid.uuid4())
            new_ids = current_ids.copy()
            new_ids[service_name] = self.requestId
            service_request_ids.set(new_ids)
        
        # Set up the logger instance.
        self.logger = logging.getLogger(service_name)
        
        # Determine log level from environment variable (defaults to INFO).
        env_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_level = getattr(logging, env_level, logging.INFO)
        self.logger.setLevel(log_level)
        
        # Clear any pre-existing handlers.
        self.logger.handlers = []
        
        # Set up a stream handler with our custom JSON formatter.
        handler = logging.StreamHandler()
        log_format = (
            '%(timestamp)s %(level)s %(service)s %(message)s '
            '%(requestId)s %(userId)s %(metadata)s'
        )
        formatter = CustomJsonFormatter(log_format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _log(self, level, message, **kwargs):
        # Always include the stored requestId and service in extra.
        extra = {'service': self.service_name, 'requestId': self.requestId}
        extra.update(kwargs)
        self.logger.log(level, message, extra=extra)

    def info(self, message, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def debug(self, message, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)
