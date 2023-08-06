#!/usr/bin/env python3

import copy
from enum import Enum


class RegistryType(Enum):
    NONE = 0

    PY = 1

    INTEGERS = 2
    FLOATS = 3
    NUMBERS = 4

    C_STRINGS = 5


class TypeRegistry:
    # NUMBERS: {'unsint': 'unsigned int*'}
    registry: dict[RegistryType, dict[str, str]] = {}

    # unsint: unsigned int*
    all_cats: dict[str, str] = {}

    # NUMBERS: [INTEGERS, FLOATS]
    auto_registry: dict[RegistryType, list[RegistryType]] = {}

    def __init__(
        self,
        registry: dict[RegistryType, dict[str, str]] | None = None,
        all_cats: dict[str, str] | None = None,
    ):
        if registry is None:
            self.registry = {}
        else:
            self.registry = copy.deepcopy(registry)

        if all_cats is None:
            self.all_cats = {}
        else:
            self.all_cats = all_cats.copy()

    def register(self, py: str, c: str, cat: RegistryType = RegistryType.NONE):
        if cat in self.registry:
            self.registry[cat][py] = c
        else:
            self.registry[cat] = {py: c}

        self._update()

    def auto_register(self, subset: RegistryType, superset: RegistryType):
        if superset in self.auto_registry:
            self.auto_registry[superset].append(subset)
        else:
            self.auto_registry[superset] = [subset]

    def copy(self) -> "TypeRegistry":
        return TypeRegistry(self.registry, self.all_cats)

    def _update(self):
        self.all_cats = {key: val for cat in self.registry.values() for key, val in cat.items()}

    def __getitem__(self, py: str) -> str:
        return self.all_cats[py]

    def __getattr__(self, cat: str) -> dict[str, str]:
        if cat not in RegistryType.__members__:
            raise AttributeError(f"Registry Type '{cat}' not found")

        if RegistryType[cat] not in self.registry:
            self.registry[RegistryType[cat]] = {}

        if RegistryType[cat] in self.auto_registry:
            return {
                key: val
                for subcat in self.auto_registry[RegistryType[cat]]
                for key, val in self.registry[subcat].items()
            } | self.registry[RegistryType[cat]]

        return self.registry[RegistryType[cat]]

    def __contains__(self, py: str) -> bool:
        return py in self.all_cats
