from termicoder.models import Testcase


class CodechefTestcase(Testcase):
    def __init__(self, inp, ans, code):
        self.inp = inp  # input
        self.ans = ans    # answer
        self.code = code  # code/number for testcase
