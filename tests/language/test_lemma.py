from language.lemma import Lemma


class TestLemmaUrl:
    def test_constructs_url(self):
        """
        It returns the dictionary url for the lemma
        """
        lemma = Lemma(text="katt")

        result = lemma.url

        assert result == "https://svenska.se/tre/?sok=katt"
