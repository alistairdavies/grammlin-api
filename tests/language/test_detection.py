from language.detection import is_swedish


class TestIsSwedish:
    def test_returns_true_for_swedish(self):
        """
        Given Swedish text
        It returns True
        """
        texts = ["Jag älskar svenska språket", "Hej, jag heter John"]

        assert all(is_swedish(text) is True for text in texts)

    def test_returns_false_for_other_language(self):
        """
        Given text in a language that is not Swedish
        It returns False
        """
        texts = [
            "I love the English language",
            "Ich liebe die deutsche Sprache",
        ]

        assert all(is_swedish(text) is False for text in texts)

    def test_returns_false_for_indistinguishable_text(self):
        """
        Given text that is unambiguous
        It returns False
        """
        text = "a"

        assert is_swedish(text) is False

    def test_returns_false_for_empty_text(self):
        """
        Given empty text
        It returns False
        """
        text = ""
        assert is_swedish(text) is False
