import unittest
from silent_jamie.engine import decide
from silent_jamie.evaluate import metrics

class PhaseZeroTests(unittest.TestCase):
    def test_question_ignored(self):
        self.assertEqual(decide({'id':'a','text':'What is the evidence?'} )['decision'],'IGNORE')
    def test_numerical_claim_selected_without_truth_verdict(self):
        r=decide({'id':'a','text':'The survey found 300 sites in 2020.'})
        self.assertEqual(r['decision'],'VERIFY_NOW')
        self.assertIsNone(r['truth_verdict'])
    def test_hedged_hypothesis_not_declared_false(self):
        r=decide({'id':'a','text':'I suspect an earlier civilization might have taught farming.'})
        self.assertEqual(r['decision'],'QUEUE')
        self.assertIsNone(r['truth_verdict'])
    def test_directive_needs_referent(self):
        self.assertEqual(decide({'id':'a','text':'Check that last date.'})['decision'],'NEEDS_CONTEXT')
    def test_no_metric_without_denominator(self):
        a={'x':{'decision':'IGNORE','critical':False}}
        b={'x':{'decision':'IGNORE','priority_0_5':0}}
        self.assertIsNone(metrics(a,b)['recall_verify_now'])
    def test_mismatch_raises(self):
        with self.assertRaises(ValueError):
            metrics({'a':{'decision':'VERIFY_NOW'}},{})

if __name__=='__main__':
    unittest.main()
