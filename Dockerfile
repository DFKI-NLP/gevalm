FROM python:3.6

ADD . ./

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python", "run_probing_experiment.py" ]
