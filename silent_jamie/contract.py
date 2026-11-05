"""Shared strict input/output contract. Transcript text is untrusted data."""
import math
DECISIONS = ('VERIFY_NOW', 'QUEUE', 'NEEDS_CONTEXT', 'IGNORE')
KINDS = ('empirical', 'numerical', 'attribution', 'hypothesis', 'opinion', 'instruction', 'other')

def number(value):
    return type(value) in (int, float) and math.isfinite(value)

def validate_segments(rows):
    seen = set()
    previous = -1
    for r in rows:
        if not isinstance(r.get('id'), str) or not r['id'] or r['id'] in seen:
            raise ValueError('Missing or duplicate segment ID')
        if not isinstance(r.get('text'), str) or not isinstance(r.get('speaker'), str):
            raise ValueError('Text and speaker must be strings')
        if not all(number(r.get(k)) for k in ('start_s', 'end_s')) or not 0 <= r['start_s'] < r['end_s'] or r['start_s'] < previous:
            raise ValueError('Invalid or nonchronological timestamps')
        seen.add(r['id'])
        previous = r['start_s']
    return rows

def validate_prediction(p, item, previous):
    required = {'segment_id','speaker','time_start_s','time_end_s','verbatim','normalized_claim','kind','decision','priority_0_5','confidence_0_1','reason','context_ids','repeat_of','requires_visual_context','truth_verdict','target_segment_id'}
    if set(p) != required:
        raise ValueError('Prediction fields differ from contract')
    for key, source in [('segment_id','id'),('speaker','speaker'),('time_start_s','start_s'),('time_end_s','end_s'),('verbatim','text')]:
        if p[key] != item[source]:
            raise ValueError('Source identity or exact span changed: '+key)
    if p['decision'] not in DECISIONS or p['kind'] not in KINDS or p['truth_verdict'] is not None:
        raise ValueError('Invalid classification or forbidden truth verdict')
    if type(p['priority_0_5']) is not int or not 0 <= p['priority_0_5'] <= 5:
        raise ValueError('Invalid priority')
    if not number(p['confidence_0_1']) or not 0 <= p['confidence_0_1'] <= 1:
        raise ValueError('Invalid confidence')
    if not isinstance(p['reason'], str) or type(p['requires_visual_context']) is not bool:
        raise ValueError('Invalid reason or visual flag')
    if not isinstance(p['context_ids'], list) or any(not isinstance(i,str) or i not in previous for i in p['context_ids']):
        raise ValueError('Unknown or future context reference')
    for k in ('repeat_of','target_segment_id'):
        if p[k] is not None and (not isinstance(p[k],str) or p[k] not in previous):
            raise ValueError('Unknown or future reference: '+k)
    if p['repeat_of'] is not None and p['decision']=='VERIFY_NOW':
        raise ValueError('A duplicate must not create another live alert')
    if p['decision'] in ('VERIFY_NOW','QUEUE') and not isinstance(p['normalized_claim'],str):
        raise ValueError('Selected candidate lacks normalized claim')
    if p['normalized_claim'] is not None and not isinstance(p['normalized_claim'],str):
        raise ValueError('Invalid claim')
    return p
