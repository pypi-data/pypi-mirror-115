"""
This module constain a new abstract type of faust record to process some data from CW api
"""

# We start importing some typing stuff
from typing import Generic, TypeVar

# and the faust related objects and types
from faust import Record
from faust.serializers import codecs

# then we import our custom codec serializer
from .._codec import digest

# and we register that codec (to be loaded for every package or script or app that use this)
codecs.register("digest", digest())

## The digest record

# We use a generic var for generic use in digests
T = TypeVar("T")


# and then we build digest that represent any 'response in list shape' throwed by the api
class Digest(Record, Generic[T], serializer="digest", abstract=True):
    digest: list[T]

    def __iter__(self):
        for d in self.digest:
            yield d

    def __str__(self) -> str:
        return str(self.digest)
