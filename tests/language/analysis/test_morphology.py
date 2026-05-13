from language.analysis.morphology import (
    AdjectiveMorphology,
    NounMorphology,
    VerbMorphology,
    PronounMorphology,
)


class TestNounMorphology_build:
    def test_returns_mapped_valid_values(self):
        """
        Given a morphology string with known values
        It returns the dataclass with sanitised values
        """
        morph = "Gender=Com|Number=Sing|Definite=Def"

        result = NounMorphology.build(morph)

        assert result == NounMorphology(
            gender="common", definiteness="definite", plurality="singular"
        )

    def test_returns_none_values_if_unknown(self):
        """
        Given a morphology string with unknown values
        It returns the dataclass with None values
        """
        morph = "Gender=something|Number=really|Definite=strange"

        result = NounMorphology.build(morph)

        assert result == NounMorphology(
            gender=None, definiteness=None, plurality=None
        )

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology string with missing values
        It returns the dataclass with None values
        """
        result = NounMorphology.build("Case=foo")

        assert result == NounMorphology(
            gender=None, definiteness=None, plurality=None
        )


class TestVerbMorphology_build:
    def test_returns_mapped_valid_values(self):
        """
        Given a morphology string with known values
        It returns the dataclass with sanitised values
        """
        morph = "Tense=Pres"

        result = VerbMorphology.build(morph)

        assert result == VerbMorphology(tense="present tense", form=None)

    def test_returns_none_values_if_unknown(self):
        """
        Given a morphology string with unknown values
        It returns the dataclass with None values
        """
        morph = "Tense=foo"

        result = VerbMorphology.build(morph)

        assert result == VerbMorphology(tense=None, form=None)

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology string with missing values
        It returns the dataclass with None values
        """
        result = VerbMorphology.build("")

        assert result == VerbMorphology(tense=None, form=None)


class TestAdjectiveMorphology_build:
    def test_returns_positive_degree(self):
        """
        Given a morphology string with known values
        It returns the dataclass with sanitised values
        """
        morph = "Degree=Pos"

        result = AdjectiveMorphology.build(morph)

        assert result == AdjectiveMorphology(degree="positive")

    def test_returns_none_if_missing(self):
        """
        Given an empty morphology string
        It returns adjective with None degree
        """
        result = AdjectiveMorphology.build("")

        assert result == AdjectiveMorphology(degree=None)

    def test_returns_none_if_unknown(self):
        """
        Given a morphology string with an unknown degree value
        It returns adjective with None degree
        """
        morph = "Degree=foo"

        result = AdjectiveMorphology.build(morph)

        assert result == AdjectiveMorphology(degree=None)


class TestPronounMorphology_build:
    def test_returns_known_values(self):
        """
        Given a morphology string with known values
        It returns the dataclass with sanitised values
        """
        morph = "Case=Nom"

        result = PronounMorphology.build(morph)

        assert result == PronounMorphology(form="subject")

    def test_returns_none_for_unknown_value(self):
        """
        Given a morphology string with an unknown case value
        It returns pronoun with possessive form as default
        """
        result = PronounMorphology.build("Case=foo|foo=bar")

        assert result == PronounMorphology(form="possessive")

    def test_returns_possessive_form_when_no_case(self):
        """
        Given a morphology string without a case field
        It returns pronoun with possessive form as default
        """
        result = PronounMorphology.build("")

        assert result == PronounMorphology(form="possessive")
