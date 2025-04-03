from dataclasses import dataclass


@dataclass
class WHISPER_MODELS:
    """Whisper models available:
    tiny - the smallest and fastest model, but with low accuracy.
    base - a balance between speed and accuracy.
    small - more accurate but slower.
    medium - high accuracy but requires more resources.
    large - the most accurate, but the slowest and most demanding on resources."""
    tiny_model: str = "tiny"
    base_model: str = "base"
    small_model: str = "small"
    medium_model: str = "medium"
    large_model: str = "large"
