import dataclasses as dc
import typing as T
from ... import streams

from . import descriptor


@dc.dataclass()
class Manifest:
    media_type: str
    config: descriptor.Descriptor = dc.field(
        default_factory=lambda: descriptor.Descriptor.empty(
            "application/vnd.oci.empty.v1+json"
        )
    )
    layers: T.List[descriptor.Descriptor] = dc.field(default_factory=list)
    annotations: T.Dict[str, str] = dc.field(default_factory=dict)

    def add_layer(self, layer: descriptor.Descriptor) -> None:
        self.layers.append(layer)

    def annotate(self, key: str, value: str) -> None:
        self.annotations[key] = value

    def blobs(self) -> T.Iterator[descriptor.Descriptor]:
        yield self.config
        yield from self.layers

class ManifestPusher(T.Protocol):
    def push_manifest(self, repository: str, reference: str, manifest: Manifest) -> None:
        ...

class ManifestPuller(T.Protocol):
    def pull_manifest(self, repository: str, reference: str) -> T.Optional[streams.Reader]:
        ...

    def does_manifest_exist(self, repository: str, reference: str) -> bool:
        ...

class ManifestPushPuller(ManifestPusher, ManifestPuller, T.Protocol):
    ...
