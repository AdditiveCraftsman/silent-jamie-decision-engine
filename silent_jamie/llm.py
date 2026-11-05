"""Optional causal selector using an OpenAI-compatible Chat Completions endpoint.
No SDK, retrieval, gold labels, implicit model choice, or rules fallback.
"""
import argparse
import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse
from .contract import validate_segments, validate_prediction

PROMPT = Path(__file__).resolve().parent.parent / 'prompts/selector_v1.txt'

def digest(value):
    return hashlib.sha256(value).hexdigest()

def make_template(item):
    return dict(segment_id=item['id'], speaker=item['speaker'], time_start_s=item['start_s'],
                time_end_s=item['end_s'], verbatim=item['text'], normalized_claim=None,
                kind='other', decision='IGNORE', priority_0_5=0, confidence_0_1=0.0,
                reason='', context_ids=[], repeat_of=None, requires_visual_context=False,
                truth_verdict=None, target_segment_id=None)

def select(rows, model, endpoint, api_key=None, window=24, transport=None):
    validate_segments(rows)
    if not model or window < 1:
        raise ValueError('Explicit model and positive window required')
    parsed = urlparse(endpoint)
    if parsed.scheme != 'https' and not (parsed.scheme=='http' and parsed.hostname in ('localhost','127.0.0.1','::1')):
        raise ValueError('Use HTTPS or loopback HTTP for a local model')
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Endpoint must not contain credentials, query or fragment')
    prompt = PROMPT.read_text(encoding='utf-8')
    predictions, calls = [], []
    for index, item in enumerate(rows):
        history = rows[max(0,index-window):index]
        visible = {r['id'] for r in history}
        payload = {'model':model, 'temperature':0, 'response_format':{'type':'json_object'},
                   'messages':[{'role':'system','content':prompt}, {'role':'user','content':json.dumps({
                       'history':history, 'previous_decisions':[p for p in predictions if p['segment_id'] in visible],
                       'current':item, 'output_template':make_template(item)}, ensure_ascii=False)}]}
        began = time.monotonic()
        if transport:
            response = transport(payload)
        else:
            headers = {'Content-Type':'application/json'}
            if api_key:
                headers['Authorization'] = 'Bearer '+api_key
            request = urllib.request.Request(endpoint, json.dumps(payload).encode(), headers)
            with urllib.request.urlopen(request, timeout=90) as reply:
                response = json.load(reply)
        choice = response['choices'][0]
        if choice.get('finish_reason') != 'stop':
            raise ValueError('Incomplete or refused model response')
        prediction = validate_prediction(json.loads(choice['message']['content']), item, visible)
        predictions.append(prediction)
        calls.append({'segment_id':item['id'], 'latency_s':round(time.monotonic()-began,4),
                      'returned_model':response.get('model'), 'usage':response.get('usage'),
                      'system_fingerprint':response.get('system_fingerprint')})
    return predictions, {'requested_model':model, 'prompt_sha256':digest(prompt.encode()),
                          'window_turns':window, 'calls':calls, 'cost_usd':None,
                          'cost_note':'Not calculated: apply documented provider rates to actual usage.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('-o','--output',type=Path,required=True)
    p.add_argument('--model',required=True)
    p.add_argument('--endpoint',default='http://localhost:11434/v1/chat/completions')
    p.add_argument('--key-env',default='SJ_API_KEY')
    p.add_argument('--window',type=int,default=24)
    a=p.parse_args()
    raw=a.input.read_bytes()
    rows=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    predictions, metadata=select(rows,a.model,a.endpoint,os.environ.get(a.key_env),a.window)
    metadata.update(input_sha256=digest(raw), prediction_sha256=digest((''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in predictions)).encode()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    # Failures do not silently produce partial benchmark files.
    a.output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in predictions),encoding='utf-8')
    a.output.with_suffix('.run.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print('Wrote predictions and run metadata; no factual verification performed.')

if __name__=='__main__':
    main()
