from lingua import Language, LanguageDetectorBuilder

_detector = (
    LanguageDetectorBuilder.from_languages(
        Language.SWEDISH,
        Language.ENGLISH,
    )
    .with_minimum_relative_distance(0.25)
    .build()
)


def is_swedish(text: str) -> bool:
    """Check if the given text is Swedish.

    Uses lingua-py which is optimized for short text detection.

    Args:
        text: The text to check

    Returns:
        True if text is detected as Swedish, False otherwise
    """
    if not text or not text.strip():
        return False

    detected = _detector.detect_language_of(text)
    return detected == Language.SWEDISH
