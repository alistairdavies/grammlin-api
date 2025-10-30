from language.morphology import NounMorphology, VerbMorphology


class TestNounMorphology_build:
    def test_returns_mapped_valid_values(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Gender": "Com", "Number": "Sing", "Definite": "Def"}

        result = NounMorphology.build(morph_dict)

        assert result == NounMorphology(
            gender="common", definiteness="definite", plurality="singular"
        )

    def test_returns_none_values_if_unknown(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Gender": "what", "Number": "is", "Definite": "this"}

        result = NounMorphology.build(morph_dict)

        assert result == NounMorphology(gender=None, definiteness=None, plurality=None)

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology dictionary with missing values
        It returns the dataclass with None values
        """
        result = NounMorphology.build({})

        assert result == NounMorphology(gender=None, definiteness=None, plurality=None)


class TestVerbMorphology_build:
    def test_returns_mapped_valid_values(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Tense": "Pres"}

        result = VerbMorphology.build(morph_dict)

        assert result == VerbMorphology(tense="present")

    def test_returns_none_values_if_unknown(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Tense": "foo"}

        result = VerbMorphology.build(morph_dict)

        assert result == VerbMorphology(tense=None)

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology dictionary with missing values
        It returns the dataclass with None values
        """
        result = VerbMorphology.build({})

        assert result == VerbMorphology(tense=None)
