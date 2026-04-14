from dataclasses import dataclass


@dataclass(frozen=True)
class QubitRegister:
    size: int
    label: str = "q"

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("QubitRegister size must be positive.")

    def __len__(self) -> int:
        return self.size


@dataclass(frozen=True)
class ClassicalRegister:
    size: int
    label: str = "c"

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("ClassicalRegister size must be positive.")

    def __len__(self) -> int:
        return self.size
