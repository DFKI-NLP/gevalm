import torch
from typing import Dict, List


class LanguageModel(object):
    """Language model wrapper that exposes interface to REST endpoints."""

    def get_mask_token(self) -> str:
        """Returns this language model's mask token."""
        raise NotImplementedError

    def get_mask_id(self) -> torch.int64:
        """Returns this language model's mask id."""
        raise NotImplementedError

    def get_unkown_token(self) -> str:
        """Returns this language model's unknown token."""
        raise NotImplementedError

    def get_unkown_id(self) -> torch.int64:
        """Returns this language model's unknown id."""
        raise NotImplementedError

    def tokenize(self, sequence: str) -> torch.Tensor:
        """Tokenizes a string of tokens, in compliance with the predict function."""
        raise NotImplementedError

    def get_token(self, idx: torch.Tensor) -> str:
        """Retrieves token at position idx from this language model's vocab."""
        raise NotImplementedError

    def get_index(self, token: str) -> torch.int64:
        """Retrieves idx of token in this language model's vocab."""
        raise NotImplementedError

    def sanitize_tokens(self, tokens: torch.Tensor) -> List[int]:
        """Turns tokens tensor into list of integers."""
        raise NotImplementedError

    def predict(self, tokens: torch.Tensor) -> (torch.Tensor, torch.Tensor):
        """
        Retrieves token probabilities and indices (for debugging purposes) from language model.
        :param tokens: List of tokens strings or ids.
        :return: Token probabilities over language model's vocabulary and input token ids.
        """
        raise NotImplementedError

    def join(self, tokens: List[str]):
        """Joins tokens in a string."""
        return ' '.join(tokens)

    def preprocess(self, sequence: str):
        mask_token = self.get_mask_token()
        sequence = sequence.replace('[MASK]', mask_token)
        return sequence

    def sample(self, sequence: str) -> str:
        """
        Replaces masked tokens in the sequence with most probable samples from this language model.
        :param sequence: String of tokens w/ optional masks.
        :return: String of tokens w/ masks replaced by samples from language model.
        """

        sequence = self.preprocess(sequence)

        tokens = self.tokenize(sequence)
        token_probabilities, token_ids = self.predict(tokens)

        tokens = self.sanitize_tokens(tokens)
        sample = []
        for idx, token in enumerate(tokens):
            if token == self.get_mask_id():
                top_token_idx = list(torch.topk(token_probabilities[idx], k=1).indices.detach())[0]
                top_token = self.get_token(top_token_idx)
                sample.append(top_token)
            else:
                assert tokens[idx] != self.get_mask_id(), 'Non-mask token was mapped on mask id.'
                token = self.get_token(tokens[idx])
                sample.append(token)

        return self.join(sample)

    # see, for instance https://www.scribendi.ai/can-we-use-bert-as-a-language-model-to-assign-score-of-a-sentence/
    def get_sequence_score(self, sequence: str) -> torch.float64:
        """Get the sequence score."""
        raise NotImplementedError

    def replace_mask_with_candidate(self, sequence: str, candidate: str):
        """Replaces the mask token in a string with the candidate string."""
        res = sequence.replace(self.get_mask_token(), candidate)
        return res

    def candidate_probabilities(self, sequence: str, candidates: str, scoring: str, verbose: bool) -> (Dict[str, float], List[str]):
        """
        Return sample probabilities for candidates as replacements for the masked tokens in the sequence.
        :param sequence: The sequence w/ masked tokens.
        :param candidates: Candidate replacementsb for the masked tokens.
        :param scoring: Scoring method ("ce": cross-entropy or "gb": goldberg)
        :param verbose: Print tokenized version to console if set to True.
        :return: Probabilities for the candidates.
        """

        candidates = candidates.split(' ')

        candidate_probabilities = {}
        cands_tokenized = []
        if scoring == "ce":
            for candidate in candidates:
                sequence_w_candidate = self.replace_mask_with_candidate(sequence, candidate)
                score, tokenized = self.get_sequence_score(sequence_w_candidate, verbose)
                candidate_probabilities[candidate] = score
                cands_tokenized.append(tokenized)

        elif scoring == "gb":
            input_ids = self.tokenize(sequence)

            tensor_input = torch.tensor(input_ids).unsqueeze(0)
            lm_out = self.language_model(tensor_input)[0]

        else:
            raise ValueError("Invalid scoring method.")

        return candidate_probabilities, cands_tokenized
