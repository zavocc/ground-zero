from types import UnionType


def validate_task(task: object, expected_type: UnionType) -> None:
    if not isinstance(task, expected_type):
        raise TypeError(f"task must be an instance of {expected_type}, got {type(task).__name__}")
