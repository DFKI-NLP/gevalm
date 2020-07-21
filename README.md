# Evaluating German Transformer Language Models with Syntactic Agreement Tests

Code and data for the paper by Karolina Zaczynska, Nils Feldhus, Robert Schwarzenberg, Aleksandra Gabryszak and Sebastian Möller:
https://arxiv.org/abs/2007.03765  
It originally appeared in the proceedings of the Swiss Text Analytics Conference & Conference on Natural Language Processing (KONVENS) 2020: http://ceur-ws.org/Vol-2624/paper7.pdf  
We recommend to refer to the more recent arXiv publication, because it includes minor adjustments.


## Data

See the `data` folder README for more information.

## Requirements
- jsonlines==1.2.0
- nltk==3.4.5
- overrides==2.8.0
- torch==1.4.0
- tqdm==4.43.0
- transformers==2.5.1
- Pattern==3.6

## Experiments

#### Run tests with LMs

Execute `python run_probing_experiment.py` with the following flags:
- `--input` : [Required]  Path to the input jsonl (directory or file). Please choose from the directories in `data/input`, e.g. `data/input/SimplSent` (whole directory) or `data/input/SimplSent/SimplSent_pl.jsonl` (single file).
- `--output_dir` : Path to the output of the experiment, by default `data/output/`. This will create a sub-folder to the one set by `--output_dir` with a name according to the language model identifier set by `--lm`. In here, you will find another sub-folder with the name corresponding to the case. That folder contains the .jsonl file(s), e.g. `data/output/bert-base-german-dbmdz-cased/SimplSent/SimplSent_pl.jsonl`. 
- `--lm` : [Required] Language model identifier, i.e. either `bert-base-german-dbmdz-cased` (our paper: gBERT_large) or `distilbert-base-german-cased` (our paper: gBERT_small)
- `--verbose` : If set, it's printing data processing steps and results in detail

#### Run evaluation on test outputs to produce accuracy scores

Execute `python evaluation.py` with the following flags:
- `--path` : [Required] Path to the output directory with .jsonl files, e.g. `data/output/bert-base-german-dbmdz-cased/SimplSent/`
- `--lm` : [Required] Language model identifier, i.e. either `bert-base-german-dbmdz-cased` (our paper: gBERT_large) or `distilbert-base-german-cased` (our paper: gBERT_small). This is for loading the correct tokenizer.
- `--sum_up_cases` : If set, it takes all .jsonl files in the directory set by `--path` and display one result for all sub-cases instead of calculating them separately.
