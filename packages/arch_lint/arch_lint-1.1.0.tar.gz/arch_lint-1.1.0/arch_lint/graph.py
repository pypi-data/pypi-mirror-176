from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
import grimp
from grimp.application.ports.graph import (
    AbstractImportGraph,
)
from importlib.util import (
    find_spec,
)
from typing import (
    cast,
    FrozenSet,
    NoReturn,
    Optional,
    Union,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class FullPathModule:
    _inner: _Private = field(repr=False, hash=False, compare=False)
    module: str

    @property
    def name(self) -> str:
        return self.module.split(".")[-1]

    @property
    def parent(self) -> Optional[FullPathModule]:
        result = ".".join(self.module.split(".")[:-1])
        return FullPathModule(_Private(), result) if result else None

    def new_child(self, module: str) -> FullPathModule:
        joined = ".".join([self.module, module])
        return FullPathModule(_Private(), joined)

    def is_descendant_of(self, module: FullPathModule) -> bool:
        if self != module:
            return self.module.startswith(module.module)
        return False

    @staticmethod
    def from_raw(raw: str) -> Union[FullPathModule, NoReturn]:
        spam_spec = find_spec(raw)
        if spam_spec is not None:
            return FullPathModule(_Private(), raw)
        raise ModuleNotFoundError(raw)


def _build_module(module: str) -> FullPathModule:
    return FullPathModule(_Private(), module)


@dataclass(frozen=True)  # type: ignore[misc]
class _ImportGraph:  # type: ignore[no-any-unimported]
    graph: AbstractImportGraph  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ImportGraph:
    _inner: _ImportGraph
    root: FullPathModule

    @staticmethod
    def build_graph(
        root_module: str, external_packages: bool
    ) -> Union[ImportGraph, NoReturn]:
        graph = grimp.build_graph(root_module, include_external_packages=external_packages)  # type: ignore[misc]
        return ImportGraph(_ImportGraph(graph), _build_module(root_module))  # type: ignore[misc]

    def chain_exists(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
        as_packages: bool,
    ) -> bool:
        return cast(
            bool,
            self._inner.graph.chain_exists(importer.module, imported.module, as_packages),  # type: ignore[misc]
        )

    def find_children(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_children(module.module))  # type: ignore[misc]
        return frozenset(_build_module(i) for i in items)

    def find_modules_that_directly_import(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_that_directly_import(module.module))  # type: ignore[misc]
        return frozenset(_build_module(i) for i in items)

    def find_modules_directly_imported_by(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_directly_imported_by(module.module))  # type: ignore[misc]
        return frozenset(_build_module(i) for i in items)
