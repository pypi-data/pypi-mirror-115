from enum import Enum


class Language(Enum):
    """
    Supported languages in this app. The short-code of the language is used as a value.
    """

    ENGLISH = {
        "valid_inputs": ("en", "EN", "english"),
        "language": "english",
        "locale": "en_GB.UTF-8",
        "languageCode": "en-GB",
    }
    """ The english language."""

    GERMAN = {
        "valid_inputs": ("de", "DE", "german", "deutsch"),
        "language": "german",
        "locale": "de_DE.UTF-8",
        "languageCode": "de-DE",
    }
    """ The german language."""


class DocumentType(Enum):
    """
    Possible types of documents for PDF-Generation.
    """

    PLAIN = "plain"
    """ A plain document, for example for a report or an article. """

    LETTER = "letter"
    """ A formatted letter to someone, from someone. """

    PRESENTATION = "presentation"
    """ A presentation with slides. """

    NEWSLETTER = "newsletter"
    """ A newsletter where all sections and the title are in fancy boxes. """
