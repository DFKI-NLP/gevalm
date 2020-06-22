import jsonlines
import os

from argparse import ArgumentParser
from sklearn.metrics import accuracy_score
from transformers import AutoTokenizer, BertTokenizer


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, required=True,
                        help='Path to either single file of jsonl or directory full of jsonl files produced by '
                             'run_probing_experiment.py')
    parser.add_argument('--lm', type=str, required=True,
                        help='Language model identifier, i.e. either "distilbert-base-german-cased" or '
                             '"bert-base-german-dbmdz-cased"')
    parser.add_argument('--sum_up_cases', action='store_true',
                        help="If set in the case of --path referring to a directory (multiple jsonl files), "
                             "accuracy is calculated for all cases together")

    args = parser.parse_args()

    try:
        tokenizer = BertTokenizer.from_pretrained(args.lm)
    except OSError:
        print('{} requires AutoTokenizer'.format(args.lm))
        tokenizer = AutoTokenizer.from_pretrained(args.lm)

    if os.path.isdir(args.path):
        all_jsonl = [os.path.join(args.path, f) for f in os.listdir(args.path)]
    elif os.path.isfile(args.path):
        all_jsonl = [args.path]
        if args.sum_up_cases:
            raise ValueError("--sum_up_cases should only be set in the case of multiple input files (--path referring "
                             "to a directory)")
    else:
        raise ValueError("--path is neither a file nor a directory.")

    y_true, y_pred = [], []
    inequal_count, equal_count = 0, 0

    for i, probing_out_file in enumerate(all_jsonl):
        case = None

        if not args.sum_up_cases:
            # create lists for overall acc
            y_true, y_pred = [], []
            inequal_count, equal_count = 0, 0

        with jsonlines.open(probing_out_file) as reader:
            for c, obj in enumerate(reader):
                # Investigate if tokenized sentence of same length achieve same results
                cand1_td = tokenizer.tokenize(obj['candidates'][0])
                cand2_td = tokenizer.tokenize(obj['candidates'][1])
                if len(cand1_td) != len(cand2_td):
                    inequal_count += 1
                    continue
                else:
                    equal_count += 1

                y_true.append(0)
                probs = list(obj['probs'].values())

                if len(probs) != 2:
                    print("Output file does not have two candidates to compare.")
                    break

                if probs[0] > probs[1]:
                    y_pred.append(1)
                else:
                    y_pred.append(0)

                if not case:
                    case = obj['case']

        if not args.sum_up_cases or i == len(all_jsonl) - 1:
            print('Ignored {} out of {} ({} %) cases of inequal tokenization length'.format(
                inequal_count, inequal_count + equal_count, 100*(inequal_count/(inequal_count + equal_count))))

            if len(probs) == 2 and len(y_true) == len(y_pred):
                if args.sum_up_cases:
                    print("total acc ({} sentences): {}".format(case, equal_count,
                                                                accuracy_score(y_true, y_pred)))
                else:
                    print("total acc for case {} ({} sentences) : {}".format(case, equal_count,
                                                                             accuracy_score(y_true, y_pred)))
            else:
                print("Invalid probing output file. Skipped {}".format(probing_out_file))
