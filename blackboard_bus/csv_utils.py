"""Shared input parsing for CSV command-line workflows."""


def parse_csv_bool(value: object) -> bool:
    """Parse a CSV boolean without treating a nonempty 'False' as true."""
    if isinstance(value, bool):
        return value
    normalized = str(value if value is not None else "").strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n", ""}:
        return False
    raise ValueError(f"Invalid is_critical_flag value: {value!r}")
