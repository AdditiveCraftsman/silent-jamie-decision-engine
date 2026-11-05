"""Freeze local input/gold provenance before any selector run. Hashes are not independence."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('input',type=Path)
p.add_argument('gold',type=Path)
p.add_argument('--annotators',nargs='+',required=True)
p.add_argument('--audio-verified',action='store_true')
p.add_argument('--split',choices=['development','holdout'],required=True)
p.add_argument('-o',type=Path,required=True)
a=p.parse_args()
record={'created_utc':datetime.now(timezone.utc).isoformat(),'split':a.split,
        'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),
        'gold_sha256':hashlib.sha256(a.gold.read_bytes()).hexdigest(),
        'annotators':a.annotators,'audio_verified_attestation':a.audio_verified,
        'note':'Attestations require review. This script cannot establish independence or source rights.'}
with a.o.open('x',encoding='utf-8') as f: json.dump(record,f,indent=2)
print('Freeze manifest created; keep raw input and labels private.')
