from dataclasses import dataclass


@dataclass
class StreamingLogsServiceContext:

    endpoint: str
    origin: str

    def __init__(self, settings):
        self.endpoint = settings['endpoint']
        self.origin = settings['origin']
