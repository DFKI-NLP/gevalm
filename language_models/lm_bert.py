import torch
import torch.nn.functional as F

from overrides import overrides
from transformers import AutoModelWithLMHead, AutoTokenizer, BertForMaskedLM, BertTokenizer
from typing import List

from language_models.lm import LanguageModel


class MaskedLanguageModelBert(LanguageModel):

    def __init__(self, pretrained_weights: str, lm_dir: str):
        super(MaskedLanguageModelBert, self).__init__()
        self._pretrained_weights: str = pretrained_weights
        self._lm_dir: str = lm_dir
        self.language_model: BertForMaskedLM = None
        self.tokenizer: BertTokenizer = None
        self._set_language_model_and_tokenizer(self._pretrained_weights)

    def _set_language_model_and_tokenizer(self, pretrained_weights: str) -> None:
        self._pretrained_weights = pretrained_weights

        try:
            self.language_model = BertForMaskedLM.from_pretrained(self._pretrained_weights, cache_dir=self._lm_dir)
            self.tokenizer = BertTokenizer.from_pretrained(self._pretrained_weights, cache_dir=self._lm_dir)
        except OSError:
            print('{} requires AutoModelWithLMHead and AutoTokenizer'.format(pretrained_weights))
            self.language_model = AutoModelWithLMHead.from_pretrained(self._pretrained_weights, cache_dir=self._lm_dir)
            self.tokenizer = AutoTokenizer.from_pretrained(self._pretrained_weights, cache_dir=self._lm_dir)
        #self.tokenizer = BertTokenizer.from_pretrained('language_models/bert-base-german-cased/vocab.txt')

    @overrides
    def get_mask_token(self) -> str:
        return self.tokenizer.mask_token

    @overrides
    def get_mask_id(self) -> torch.int64:
        return self.tokenizer.mask_token_id

    @overrides
    def get_unkown_token(self) -> str:
        return self.tokenizer.unk_token

    @overrides
    def get_unkown_id(self) -> torch.int64:
        return self.tokenizer.unk_token_id

    @overrides
    def tokenize(self, sequence: str) -> List:
        return self.tokenizer.encode(sequence, add_special_tokens=True, return_tensors="pt")

    @overrides
    def get_token(self, idx: torch.Tensor) -> str:
        token = self.tokenizer.decode([idx])
        return token

    @overrides
    def get_index(self, token: str) -> int:
        idx = self.tokenizer.encode(text=[token], add_special_tokens=False)
        return idx[0]

    @overrides
    def sanitize_tokens(self, tokens: torch.Tensor) -> List[int]:
        return tokens[0].tolist()

    @overrides
    def predict(self, tokens: torch.Tensor) -> (torch.Tensor, torch.Tensor):
        with torch.no_grad():
            logits = self.language_model(tokens)[0][0]
        probabilities = F.softmax(logits, dim=1).detach()
        input_token_ids = tokens[0].detach()
        assert (len(probabilities) == len(input_token_ids)), 'Sanity check failed, dimensions do not match.'
        return probabilities, input_token_ids

    # see, for instance https://www.scribendi.ai/can-we-use-bert-as-a-language-model-to-assign-score-of-a-sentence/
    @overrides
    def get_sequence_score(self, sequence: str, verbose: bool) -> (torch.float64, List[str]):
        token_ids_input = [self.tokenizer.encode(sequence, add_special_tokens=True)]
        tokenized = [self.tokenizer.convert_ids_to_tokens(tok) for tok in token_ids_input]
        if verbose:
            print(tokenized)

        tensor_input = torch.tensor(token_ids_input)#.unsqueeze(0)
        predictions = self.language_model(tensor_input)[0]
        loss_fct = torch.nn.CrossEntropyLoss()
        loss = loss_fct(predictions.squeeze(), tensor_input.squeeze()).data
        loss = loss.item()
        return loss, tokenized
