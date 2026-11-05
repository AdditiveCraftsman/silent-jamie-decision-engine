"""Turn-level triage evaluation. Does not measure truth or atomic extraction recall."""
import argparse
import json
from pathlib import Path
from .contract import DECISIONS

def load(path):
    rows=[json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]
    result={r.get('id',r.get('segment_id')):r for r in rows}
    if len(result)!=len(rows) or None in result:
        raise ValueError('Duplicate or missing IDs: '+str(path))
    return result

def ratio(n,d):
    return {'numerator':n,'denominator':d,'value':round(n/d,4) if d else None}

def metrics(gold,pred,duration_s=None):
    if set(gold)!=set(pred):
        raise ValueError('Prediction coverage mismatch')
    for row in list(gold.values())+list(pred.values()):
        if row.get('decision') not in DECISIONS or type(row.get('priority_0_5',0)) is not int or not 0 <= row.get('priority_0_5',0) <= 5:
            raise ValueError('Invalid evaluation row')
    if duration_s is not None and duration_s <= 0:
        raise ValueError('Duration must be positive')
    positives={i for i,r in gold.items() if r['decision']=='VERIFY_NOW'}
    selected={i for i,r in pred.items() if r['decision']=='VERIFY_NOW'}
    correct=positives & selected
    critical={i for i,r in gold.items() if r.get('critical',False)}
    ranked=sorted(selected,key=lambda i:(-pred[i]['priority_0_5'],i))[:5]
    confusion={g:{p:0 for p in DECISIONS} for g in DECISIONS}
    for i in gold:
        confusion[gold[i]['decision']][pred[i]['decision']]+=1
    tasks={tag:[i for i,r in gold.items() if tag in r.get('tags',[])] for tag in ('instruction','context','duplicate','restraint','quote','visual','bilingual')}
    diagnostics={tag:ratio(sum(gold[i]['decision']==pred[i]['decision'] for i in ids),len(ids)) for tag,ids in tasks.items()}
    directed=[i for i,r in gold.items() if 'target_segment_id' in r]
    attributed=[i for i in selected if gold[i].get('speaker') not in (None,'unknown')]
    repeats=[i for i,r in gold.items() if r.get('repeat_of')]
    return {'n_segments':len(gold),'n_gold_verify_now':len(positives),'n_predicted_verify_now':len(selected),
            'precision_verify_now':ratio(len(correct),len(selected))['value'],
            'recall_verify_now':ratio(len(correct),len(positives))['value'],
            'precision_at_5':ratio(sum(i in positives for i in ranked),5)['value'] if ranked else None,
            'precision_at_returned':ratio(sum(i in positives for i in ranked),len(ranked)),
            'shortlist_size':len(ranked),'shortlist_ids':ranked,
            'critical_recall':ratio(len(critical & selected),len(critical))['value'],
            'denominators':{'precision':len(selected),'recall':len(positives),'critical_recall':len(critical)},
            'false_live_alerts':len(selected-positives),
            'false_live_alerts_per_10_min':round(len(selected-positives)*600/duration_s,4) if duration_s else None,
            'false_live_alert_ids':sorted(selected-positives),'missed_critical_ids':sorted(critical-selected),
            'confusion_gold_rows_prediction_columns':confusion,'diagnostic_decision_accuracy':diagnostics,
            'directed_target_accuracy':ratio(sum(pred[i].get('target_segment_id')==gold[i]['target_segment_id'] and pred[i]['decision']==gold[i]['decision'] for i in directed),len(directed)),
            'selected_speaker_accuracy':ratio(sum(pred[i].get('speaker')==gold[i]['speaker'] for i in attributed),len(attributed)),
            'duplicate_live_alert_ids':[i for i in repeats if i in selected],
            'repeat_link_accuracy':ratio(sum(pred[i].get('repeat_of')==gold[i]['repeat_of'] for i in repeats),len(repeats)),
            'failures':[{'id':i,'gold':gold[i]['decision'],'predicted':pred[i]['decision']} for i in gold if gold[i]['decision']!=pred[i]['decision']],
            'limitations':['Turn-level classification only; atomic claims may be missed within a turn.',
                           'Speaker score is metadata preservation, not audio diarization.',
                           'Context/quote semantics and priority ranks require blinded human review.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('gold',type=Path)
    p.add_argument('predictions',type=Path)
    p.add_argument('--duration-s',type=float)
    a=p.parse_args()
    print(json.dumps(metrics(load(a.gold),load(a.predictions),a.duration_s),indent=2))

if __name__=='__main__':
    main()
