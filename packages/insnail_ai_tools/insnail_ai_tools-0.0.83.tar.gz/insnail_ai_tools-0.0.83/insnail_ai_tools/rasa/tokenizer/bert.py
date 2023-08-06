from typing import List, Text

from rasa.nlu.tokenizers.tokenizer import Token
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from rasa.nlu.utils.hugging_face.registry import model_weights_defaults
from rasa.shared.nlu.constants import ENTITIES
from rasa.shared.nlu.training_data.message import Message
from transformers.tokenization_bert import BertTokenizerFast

model_weights = model_weights_defaults["bert"]
cache_dir = None

tokenizer = BertTokenizerFast.from_pretrained(model_weights, cache_dir=cache_dir)


class CustomBertFastTokenizer(WhitespaceTokenizer):
    """
    LanguageModelFeaturizer 会使用 BertTokenizer，故采用BertTokenizerFast作为基础tokenizer。
    CustomBertFastTokenizer的tokenize是使用BertTokenizerFast作为基础的token工具，会结合预先的实体标注信息做token操作。避免tag不能对其
    """

    supported_language_list = ["zh"]
    not_supported_language_list = None

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        entities = message.get(ENTITIES)
        if not entities:
            tokens = []
            text = message.get(attribute)
            words = tokenizer.tokenize(text)
            offset = tokenizer.encode_plus(text, return_offsets_mapping=True)[
                "offset_mapping"
            ]
            for w, ix in zip(words, offset[1:-1]):
                tokens.append(Token(w, start=ix[0], end=ix[1]))
        else:

            origin_text = message.get(attribute)

            text_list = []
            for i, entity in enumerate(entities):
                if i == 0:
                    if entity["start"] == 0:
                        text_list.append(entity["value"])
                    else:
                        text_list.append(origin_text[0 : entity["start"]])
                        text_list.append(entity["value"])
                elif i == (len(entities) - 1):
                    pre_entity = entities[i - 1]
                    text_list.append(origin_text[pre_entity["end"] : entity["start"]])
                    if entity["end"] == len(origin_text):
                        text_list.append(entity["value"])
                    else:
                        text_list.append(entity["value"])
                        text_list.append(origin_text[entity["end"] :])
                else:
                    pre_entity = entities[i - 1]
                    text_list.append(origin_text[pre_entity["end"] : entity["start"]])
                    text_list.append(entity["value"])

            tokens = []
            for i, text in enumerate(text_list):
                off_len = len("".join(text_list[:i]))
                words = tokenizer.tokenize(text)
                offset = tokenizer.encode_plus(text, return_offsets_mapping=True)[
                    "offset_mapping"
                ]
                for w, ix in zip(words, offset[1:-1]):
                    tokens.append(Token(w, start=ix[0] + off_len, end=ix[1] + off_len))

        return self._apply_token_pattern(tokens)
