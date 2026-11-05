"""Simple offline rules baseline. NOT a trained classifier or a fact checker."""
import argparse
import json
import re
from pathlib import Path

NUMBER = re.compile(r"\b(?:\d[\d,]*(?:\.\d+)?|\d{4})\b")
FACT_TERMS = re.compile(r"\b(?:study|report|survey|lab|paper|published|retracted|dated|records|according to|researchers|measured|found)\b", re.I)
HYPOTHESIS = re.compile(r"\b(?:suspect|might have|perhaps|hypothesis|could have)\b", re.I)
PERSONAL = re.compile(r"\b(?:i prefer|i grew|i feel|i like)\b", re.I)
COMMAND = re.compile(r"\b(?:check that|verify that|fact.check that|look that up)\b", re.I)


def decide(item):
    """Return a transparent but intentionally weak decision for one segment."""
    text = str(item.get('text', '')).strip()
    if not text:
        d, p, why = 'IGNORE', 0, 'Empty segment'
    elif COMMAND.search(text):
        d, p, why = 'NEEDS_CONTEXT', 0, 'Directed check: must resolve referent from previous turns'
    elif text.endswith('?'):
        d, p, why = 'IGNORE', 0, 'Non-assertive question'
    elif PERSONAL.search(text):
        d, p, why = 'IGNORE', 0, 'Opinion or private anecdote'
    elif HYPOTHESIS.search(text):
        d, p, why = 'QUEUE', 3, 'Speculative claim; assess evidentiary basis without assuming falsehood'
    elif NUMBER.search(text) or FACT_TERMS.search(text):
        d, p, why = 'VERIFY_NOW', 4, 'Specific public factual assertion candidate'
    else:
        d, p, why = 'IGNORE', 0, 'No high-specificity factual trigger detected'
    return {'segment_id':item.get('id'), 'speaker':item.get('speaker','unknown'),
            'time_start_s':item.get('start_s'), 'time_end_s':item.get('end_s'),
            'verbatim':text, 'normalized_claim':text if d in {'VERIFY_NOW','QUEUE'} else None,
            'decision':d, 'priority_0_5':p, 'reason':why, 'truth_verdict':None,
            'engine':'deterministic-baseline-v0.1'}


def main():
    parser = argparse.ArgumentParser(description='Offline transcript claim-selection baseline')
    parser.add_argument('input',type=Path,help='JSONL transcript segments')
    parser.add_argument('-o','--output',type=Path,required=True,help='Prediction JSONL output')
    a = parser.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.input.open(encoding='utf-8') as fin, a.output.open('w', encoding='utf-8') as fout:
        for line in fin:
            if line.strip():
                pred=decide(json.loads(line))
                fout.write(json.dumps(pred,ensure_ascii=False)+'\n')
    print(f'Wrote {a.output}')

if __name__=='__main__':
    main()
