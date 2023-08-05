import typing


TASK_TYPES: typing.List[str] = [
    "IntegrationTask",
    "QueueTask",
    "AnalyticsTask",
    "t" # Used for testing only.
]

MAPPING_ENTITIES: typing.List[str] = ['Installations', 'Devices/Sensors', 'Readings', 'Work Orders']