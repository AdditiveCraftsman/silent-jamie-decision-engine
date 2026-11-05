"""Small benchmark reporter. Designed for frozen, human-labeled datasets."""
import argparse
import json
from pathlib import Path


def load(path):
    with Path(path).open(encoding='utf-8') as f:
        data=[json.loads(line) for line in f if line.strip()]
    key=lambda x: x.get('id',x.get('segment_id'))
    out={key(r):r for r in data}
    if len(out)!=len(data) or None in out:
        raise ValueError(f'Duplicate or missing IDs in {path}')
    return out


def metrics(gold,pred):
    absent=sorted(set(gold)-set(pred))
    unexpected=sorted(set(pred)-set(gold))
    if absent or unexpected:
        raise ValueError(f'Prediction coverage mismatch: missing={absent} extra={unexpected}')
    positives={i for i,r in gold.items() if r['decision']=='VERIFY_NOW'}
    predicted={i for i,r in pred.items() if r['decision']=='VERIFY_NOW'}
    correct=positives & predicted
    ranked=sorted(pred, key=lambda i:(pred[i].get('priority_0_5',0),pred[i]['decision']=='VERIFY_NOW'),reverse=True)
    top5=ranked[:5]
    critical={i for i,r in gold.items() if r.get('critical',False)}
    return {'n_segments':len(gold),'n_gold_verify_now':len(positives),
            'n_predicted_verify_now':len(predicted),
            'precision_verify_now':round(len(correct)/len(predicted),3) if predicted else None,
            'recall_verify_now':round(len(correct)/len(positives),3) if positives else None,
            'precision_at_5':round(sum(i in positives for i in top5)/len(top5),3) if top5 else None,
            'critical_recall':round(len(critical & predicted)/len(critical),3) if critical else None,
            'false_live_alerts':len(predicted-positives),
            'false_live_alert_ids':sorted(predicted-positives),
            'missed_critical_ids':sorted(critical-predicted)}


def main():
    parser=argparse.ArgumentParser(description='Compare selector predictions to frozen human labels')
    parser.add_argument('gold',type=Path)
    parser.add_argument('predictions',type=Path)
    a=parser.parse_args()
    print(json.dumps(metrics(load(a.gold),load(a.predictions)),indent=2))
    print('NOTE: Synthetic fixture results are sanity checks, not real-world accuracy.')

if __name__=='__main__':
    main()
