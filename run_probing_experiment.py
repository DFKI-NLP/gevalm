import io
import json
import os

from argparse import ArgumentParser
from tqdm import tqdm

from language_models.lm_bert import MaskedLanguageModelBert


def probe(input_path, out_dir, cache_dir, lm, verbose, scoring='ce'):
    assert os.path.exists(out_dir)

    if os.path.isdir(lm):
        print('Language model is present in project directory.')

    if '/' in lm:
        lm_out_dir = os.path.join(out_dir, '_'.join(lm.split('/')))
    else:
        lm_out_dir = os.path.join(out_dir, lm)
    if not os.path.exists(lm_out_dir):
        os.makedirs(lm_out_dir)
        print('Created {}'.format(lm_out_dir))

    if input_path.endswith('/'):
        input_path = input_path.rstrip('/')
    case_lm_out_dir = os.path.join(lm_out_dir, input_path.split('/')[-1])
    if not os.path.exists(case_lm_out_dir):
        os.makedirs(case_lm_out_dir)
        print('Created {}'.format(case_lm_out_dir))

    # Retrieve files
    all_inputs = []
    if os.path.isdir(input_path):
        for input_path_file in os.listdir(input_path):
            all_inputs.append(os.path.join(input_path, input_path_file))
    print('Found files: {}'.format(all_inputs))

    all_cases = []
    for input_file in all_inputs:
        # Read single file
        fin = io.open(input_file, 'r', encoding='utf-8')
        fin_lines = fin.readlines()

        # Collect all sub-cases
        for idx, line in enumerate(fin_lines):
            json_line = json.loads(line.strip())

            case = json_line['case']
            if case not in all_cases:
                all_cases.append(case)
    print('Found cases: {}'.format(all_cases))

    # Create subdirectory of cache_dir for type of language model
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        print('Created cache directory: {}'.format(cache_dir))
    lm_cache_dir = os.path.join(cache_dir, lm)
    if not os.path.exists(lm_cache_dir):
        os.makedirs(lm_cache_dir)
        print('Created cache subdirectory {} for language model {}'.format(lm_cache_dir, lm))

    # Do for all sub cases
    for case, input_file in zip(all_cases, all_inputs):
        out_filename = os.path.join(case_lm_out_dir, 'out_{}.jsonl'.format(case))
        fout = io.open(out_filename, 'w+', encoding='utf-8')

        fin = io.open(input_file, 'r', encoding='utf-8')
        fin_lines = fin.readlines()

        # Load language model
        model = MaskedLanguageModelBert(lm, lm_cache_dir)
        print('Running {} with {}'.format(input_file, lm))
        for idx, line in tqdm(enumerate(fin_lines), total=len(fin_lines)):
            json_line = json.loads(line.strip())
            sequence = json_line['text_masked']
            candidates = json_line['candidates']
            candidates = ' '.join(candidates)
            probs, tokenized = model.candidate_probabilities(sequence, candidates, scoring, verbose)
            if verbose:
                print(f'{idx}) sequence: {sequence}')
                print(f'{idx}) candidates: {candidates}')
                print(f'{idx}) probs: {probs}')
                print()
            json_line['probs'] = probs
            json_line['tokenized'] = tokenized
            fout.write(json.dumps(json_line) + os.linesep)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, required=True,
                        help='Path to the input jsonl (directory or file).')
    parser.add_argument('--output_dir', type=str, default='data/output',
                        help='Path to the output jsonl (directory or file).')
    parser.add_argument('--cache_dir', type=str, default='models',
                        help='Path to directory for storing the language models')
    parser.add_argument('--lm', type=str,
                        help='Type of language model (identifier)')
    parser.add_argument('--scoring', type=str, default='ce',
                        help='Choose between "ce" (cross-entropy) or "goldberg" for way of scoring sentences')
    parser.add_argument('--verbose', action='store_true',
                        help='Whether or not to log verbosely.')
    args = parser.parse_args()

    probe(input_path=args.input, out_dir=args.output_dir, cache_dir=args.cache_dir, lm=args.lm, verbose=args.verbose,
          scoring=args.scoring)
