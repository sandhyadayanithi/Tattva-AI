import re


def normalize_transcript(text: str) -> str:
    """
    Normalizes a raw transcript so that cache comparisons are consistent.

    Steps:
    1. Convert to lowercase
    2. Strip leading/trailing whitespace
    3. Collapse duplicate whitespace into a single space
    4. Remove unnecessary punctuation (keeps alphanumeric and basic sentence chars)
    """
    if not text:
        return ""
    normalized = text.lower()
    normalized = normalized.strip()
    # Remove characters that are not alphanumeric, space, or essential punctuation
    normalized = re.sub(r"[^a-z0-9\u0900-\u097f\u0b80-\u0bff\u0c00-\u0c7f\u0980-\u09ff\s]", "", normalized)
    # Collapse multiple spaces into one
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip()
    return normalized
