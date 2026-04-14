from dataclasses import dataclass
from typing import Iterator, List, Union


@dataclass(frozen=True)
class QubitRef:
    index: int
    register: str = "q"

    def __str__(self) -> str:
        return f"{self.register}[{self.index}]"


@dataclass(frozen=True)
class BitRef:
    index: int
    register: str = "c"

    def __str__(self) -> str:
        return f"{self.register}[{self.index}]"


class QubitRegister:
    def __init__(self, size: int, label: str = "q"):
        if size <= 0:
            raise ValueError("QubitRegister size must be positive.")
        self.size = size
        self.label = label
        self._refs = [QubitRef(index=index, register=label) for index in range(size)]

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> QubitRef:
        return self._refs[index]

    def __iter__(self) -> Iterator[QubitRef]:
        return iter(self._refs)

    def to_list(self) -> List[QubitRef]:
        return list(self._refs)


class ClassicalRegister:
    def __init__(self, size: int, label: str = "c"):
        if size <= 0:
            raise ValueError("ClassicalRegister size must be positive.")
        self.size = size
        self.label = label
        self._refs = [BitRef(index=index, register=label) for index in range(size)]

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> BitRef:
        return self._refs[index]

    def __iter__(self) -> Iterator[BitRef]:
        return iter(self._refs)

    def to_list(self) -> List[BitRef]:
        return list(self._refs)


QubitLike = Union[int, QubitRef]
BitLike = Union[int, BitRef]
