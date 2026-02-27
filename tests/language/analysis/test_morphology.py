from language.analysis.morphology import (
    AdjectiveMorphology,
    NounMorphology,
    VerbMorphology,
    PronounMorphology,
)


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

        assert result == NounMorphology(
            gender=None, definiteness=None, plurality=None
        )

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology dictionary with missing values
        It returns the dataclass with None values
        """
        result = NounMorphology.build({})

        assert result == NounMorphology(
            gender=None, definiteness=None, plurality=None
        )


class TestVerbMorphology_build:
    def test_returns_mapped_valid_values(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Tense": "Pres"}

        result = VerbMorphology.build(morph_dict)

        assert result == VerbMorphology(tense="present tense", form=None)

    def test_returns_none_values_if_unknown(self):
        """
        Given a morphology dictionary with known values
        It returns the dataclass with sanitised values
        """
        morph_dict = {"Tense": "foo"}

        result = VerbMorphology.build(morph_dict)

        assert result == VerbMorphology(tense=None, form=None)

    def test_returns_none_values_if_missing(self):
        """
        Given a morphology dictionary with missing values
        It returns the dataclass with None values
        """
        result = VerbMorphology.build({})

        assert result == VerbMorphology(tense=None, form=None)


class TestAdjectiveMorphology_build:
    def test_returns_positive_degree(self):
        """
        Given a morphology dictionary with positive degree
        It returns adjective with positive degree
        """
        morph_dict = {"Degree": "Pos"}

        result = AdjectiveMorphology.build(morph_dict)

        assert result == AdjectiveMorphology(degree="positive")

    def test_returns_comparative_degree(self):
        """
        Given a morphology dictionary with comparative degree
        It returns adjective with comparative degree
        """
        morph_dict = {"Degree": "Cmp"}

        result = AdjectiveMorphology.build(morph_dict)

        assert result == AdjectiveMorphology(degree="comparative")

    def test_returns_superlative_degree(self):
        """
        Given a morphology dictionary with superlative degree
        It returns adjective with superlative degree
        """
        morph_dict = {"Degree": "Sup"}

        result = AdjectiveMorphology.build(morph_dict)

        assert result == AdjectiveMorphology(degree="superlative")

    def test_returns_none_if_missing(self):
        """
        Given an empty morphology dictionary
        It returns adjective with None degree
        """
        result = AdjectiveMorphology.build({})

        assert result == AdjectiveMorphology(degree=None)

    def test_returns_none_if_unknown(self):
        """
        Given a morphology dictionary with an unknown degree value
        It returns adjective with None degree
        """
        morph_dict = {"Degree": "foo"}

        result = AdjectiveMorphology.build(morph_dict)

        assert result == AdjectiveMorphology(degree=None)


class TestPronounMorphology_build:
    def test_returns_subject_form(self):
        """
        Given a morphology dictionary with nominative case
        It returns pronoun with subject form
        """
        morph_dict = {"Case": "Nom"}

        result = PronounMorphology.build(morph_dict)

        assert result == PronounMorphology(form="subject")

    def test_returns_object_form(self):
        """
        Given a morphology dictionary with accusative case
        It returns pronoun with object form
        """
        morph_dict = {"Case": "Acc"}

        result = PronounMorphology.build(morph_dict)

        assert result == PronounMorphology(form="object")

    def test_returns_possessive_form_when_no_case(self):
        """
        Given a morphology dictionary without a case field
        It returns pronoun with possessive form as default
        """
        result = PronounMorphology.build({})

        assert result == PronounMorphology(form="possessive")
