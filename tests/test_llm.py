import copy
import json
import unittest
from silent_jamie.llm import make_template, select
from silent_jamie.contract import validate_prediction, validate_segments

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.rows=[{'id':'a','speaker':'A','text':'A report found 20 sites.','start_s':0,'end_s':3},
                   {'id':'b','speaker':'B','text':'Jamie, check that.','start_s':3,'end_s':5}]
    def test_causal_and_no_gold(self):
        payloads=[]
        def fake(payload):
            payloads.append(payload)
            data=json.loads(payload['messages'][1]['content'])
            prediction=data['output_template']
            return {'model':'mock-contract-only','choices':[{'finish_reason':'stop','message':{'content':json.dumps(prediction)}}]}
        predictions,meta=select(self.rows,'mock','http://localhost:11434/v1/chat/completions',transport=fake)
        first=json.loads(payloads[0]['messages'][1]['content'])
        self.assertEqual(first['history'],[])
        self.assertEqual(first['current']['id'],'a')
        self.assertEqual(first['previous_decisions'],[])
        second=json.loads(payloads[1]['messages'][1]['content'])
        self.assertEqual([r['id'] for r in second['history']],['a'])
        self.assertNotIn('gold',second)
        self.assertEqual(len(meta['calls']),2)
    def test_output_mutations_rejected(self):
        p=make_template(self.rows[1])
        for field,value in [('verbatim','fabricated'),('speaker','A'),('truth_verdict','false'),('context_ids',['future']),('target_segment_id','future'),('priority_0_5',True),('confidence_0_1',float('nan'))]:
            q=copy.deepcopy(p); q[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_prediction(q,self.rows[1],{'a'})
    def test_duplicate_alert_rejected(self):
        p=make_template(self.rows[1]);p.update(decision='VERIFY_NOW',repeat_of='a')
        with self.assertRaises(ValueError): validate_prediction(p,self.rows[1],{'a'})
    def test_failure_not_baseline_fallback(self):
        def broken(payload): raise RuntimeError('model offline')
        with self.assertRaises(RuntimeError): select(self.rows,'mock','http://localhost:1234',transport=broken)
    def test_truncation_rejected(self):
        def fake(payload): return {'choices':[{'finish_reason':'length','message':{'content':'{}'}}]}
        with self.assertRaises(ValueError): select(self.rows,'mock','http://localhost:1234',transport=fake)
    def test_input_validation(self):
        for rows in [self.rows+[self.rows[0]], [dict(self.rows[0],end_s=-1)],list(reversed(self.rows))]:
            with self.assertRaises(ValueError): validate_segments(rows)
    def test_endpoint_validation(self):
        with self.assertRaises(ValueError): select(self.rows,'mock','http://external.example/v1',transport=lambda p:None)
