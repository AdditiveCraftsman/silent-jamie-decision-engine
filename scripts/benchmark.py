"""Reproduce ONLY original synthetic fixture results; never a real-world benchmark."""
import hashlib
import json
import platform
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from silent_jamie.engine import decide
from silent_jamie.evaluate import load,metrics
root=Path(__file__).resolve().parents[1]
fixture=root/'data/fixtures/synthetic.jsonl'
gold=root/'data/fixtures/synthetic_gold.jsonl'
rows=[json.loads(s) for s in fixture.read_text().splitlines() if s.strip()]
pred={r['id']:decide(r) for r in rows}
result={'dataset':'starter-synthetic','evidence_class':'synthetic sanity check, NOT real-world performance',
        'engine':'deterministic-baseline-v0.1','python':platform.python_version(),
        'input_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),
        'gold_sha256':hashlib.sha256(gold.read_bytes()).hexdigest(),
        'metrics':metrics(load(gold),pred,60),
        'llm_status':'NOT RUN; no configured endpoint or credentials',
        'human_reference_status':'not prepared; existing synthetic illustrative labels only'}
out=root/'reports/synthetic-baseline.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
