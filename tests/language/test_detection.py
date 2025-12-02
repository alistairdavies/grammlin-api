from language.detection import is_swedish


class TestIsSwedish:
    def test_returns_true_for_swedish(self):
        """
        Given Swedish text
        When checking if Swedish
        Then returns True
        """
        text = "Jag älskar svenska språket"
        assert is_swedish(text) is True

    def test_returns_false_for_english(self):
        """
        Given English text
        When checking if Swedish
        Then returns False
        """
        text = "I love the English language"
        assert is_swedish(text) is False

    def test_returns_false_for_german(self):
        """
        Given German text
        When checking if Swedish
        Then returns False
        """
        text = "Ich liebe die deutsche Sprache"
        assert is_swedish(text) is False

    def test_returns_false_when_detection_fails(self):
        """
        Given text that cannot be detected
        When checking if Swedish
        Then returns False
        """
        text = "a"
        assert is_swedish(text) is False

    def test_returns_false_for_empty_text(self):
        """
        Given empty text
        When checking if Swedish
        Then returns False
        """
        text = ""
        assert is_swedish(text) is False
