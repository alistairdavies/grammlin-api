from language.analysis.part_of_speech import map_universal_pos


class TestMapUniversalPOS:
    def test_valid_pos_tag(self):
        """
        Given a valid universal tag
        It returns the corresponding PartOfSpeechId
        """
        tag = "NOUN"

        result = map_universal_pos(tag)

        assert result == "noun"

    def test_invalid_pos_tag(self):
        """
        Given an invalid or unknown tag
        It returns None
        """
        tag = "invalid gibberish"

        result = map_universal_pos(tag)

        assert result is None
