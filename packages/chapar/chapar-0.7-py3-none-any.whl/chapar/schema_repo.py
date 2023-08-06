from pkg_resources import require
from pulsar.schema import (
    Record,
    String,
    Array,
    Float,
)


class TextItem(Record):
    uuid = String(required=True)
    text = String()
    sequence_id = String()


class TextSchema(Record):
    items = Array(TextItem(), required=True)


class TextEmbeddingItem(Record):
    uuid = String(required=True)
    text = String()
    embedding = Array(Float())


class TextEmbeddingSchema(Record):
    items = Array(TextEmbeddingItem(), required=True)


class TaskSchema(Record):
    task_class = String(required=True)
    task_id = String()
    job_id = String()
    args = String()
    kwargs = String()
