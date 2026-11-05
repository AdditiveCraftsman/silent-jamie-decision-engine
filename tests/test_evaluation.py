import unittest
from silent_jamie.evaluate import metrics
class EvaluationTests(unittest.TestCase):
    def test_ignore_never_enters_shortlist(self):
        gold={'a':{'decision':'IGNORE'}}
        prediction={'a':{'decision':'IGNORE','priority_0_5':5}}
        r=metrics(gold,prediction,60)
        self.assertEqual(r['shortlist_ids'],[])
        self.assertIsNone(r['precision_at_5'])
    def test_p5_does_not_reward_undersupply(self):
        gold={'a':{'decision':'VERIFY_NOW','critical':True}}
        prediction={'a':{'decision':'VERIFY_NOW','priority_0_5':5}}
        r=metrics(gold,prediction,60)
        self.assertEqual(r['precision_at_5'],0.2)
        self.assertEqual(r['precision_at_returned']['value'],1)
    def test_false_alert_rate_and_target(self):
        gold={'a':{'decision':'IGNORE','target_segment_id':None}}
        prediction={'a':{'decision':'VERIFY_NOW','priority_0_5':5,'target_segment_id':None}}
        r=metrics(gold,prediction,300)
        self.assertEqual(r['false_live_alerts_per_10_min'],2)
        self.assertEqual(r['directed_target_accuracy']['value'],0)
