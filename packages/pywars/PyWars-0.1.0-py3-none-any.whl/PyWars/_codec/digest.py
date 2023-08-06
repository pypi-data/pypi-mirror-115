from typing import Any

from faust import Codec
from faust.serializers import codecs


class digest(Codec):
    predecesor = codecs.json()

    def _dumps(self, s) -> bytes:
        digest = s["digest"]
        return self.predecesor._dumps(digest)

    def _loads(self, s: bytes) -> Any:
        digest = self.predecesor._loads(s)
        return {"digest": digest}
