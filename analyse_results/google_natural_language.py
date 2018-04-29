# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="data.."

def get_entities(question):
    # Instantiates a client
    text = question.text
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document).entities
    # tokens = client.analyze_syntax(document).tokens
    #
    # # part-of-speech tags from enums.PartOfSpeech.Tag
    # pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
    #            'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
    #
    # for token in tokens:
    #     print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
    #                            token.text.content))

    entity_names = []
    for entity in entities:
        entity_name = entity.name
        entity_names.append(entity_name)

    return entity_names
#
# def syntax_text(text):
#     """Detects syntax in the text."""
#     client = language.LanguageServiceClient()
#     # Instantiates a plain text document.
#     document = types.Document(
#         content=text,
#         type=enums.Document.Type.PLAIN_TEXT)
#
#     # Detects syntax in the document. You can also analyze HTML with:
#     #   document.type == enums.Document.Type.HTML
#
#     #
#     # print('Text: {}'.format(text))
#     # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
