import unittest
from Parser import Parser
from solver import InverseFuzzyInference


class TestSolver(unittest.TestCase):
    def test1(self):
        '''
        A = {<y1, 0.6>, <y2, 0.1>, <y3, 0.3>}

        R(x) = {<<x1,y1>, 0.6>, <<x1,y2>, 0.1>, <<x1,y3>, 0.4>, <<x2,y1>, 0.6>, <<x2,y2>, 0.1>, <<x2,y3>, 0.1>}
        '''
        with open('inputs/input1.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, '<C(x1),C(x2)> ∈ (0.3 × [0.6, 1.0]) ')


    def test2(self):
        '''
        A = {<y1, 0.7>, <y2, 0.1>, <y3, 0.3>}

        R(x) = {<<x1,y1>, 0.7>, <<x1,y2>, 0.1>, <<x1,y3>, 0.4>, <<x2,y1>, 0.8>, <<x2,y2>, 0.1>, <<x2,y3>, 0.1>}
        '''
        with open('inputs/input2.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, '<C(x1),C(x2)> ∈ (0.3 × 0.7) ')

    def test3(self):
        '''
        A = {<y1, 0.6>, <y2, 0.2>, <y3, 0.2>}

        R(x) = {<<x1,y1>, 0.7>, <<x1,y2>, 0.1>, <<x1,y3>, 0.1>, <<x2,y1>, 0.5>, <<x2,y2>, 0.1>, <<x2,y3>, 0.1>}
        '''
        with open('inputs/input3.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, 'Нельзя построить обратный вывод!')

    def test4(self):
        '''
        A = {<y1, 0.6>, <y2, 0.2>, <y3, 0.2>}

        R(x) = {<<x1,y1>, 0.7>, <<x1,y2>, 0.6>, <<x1,y3>, 0.9>, <<x2,y1>, 0.7>, <<x2,y2>, 0.5>, <<x2,y3>, 0.3>, <<x3,y1>, 0.8>, <<x3,y2>, 0.4>, <<x3,y3>, 0.3>}
        '''
        with open('inputs/input4.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, 'Нельзя построить обратный вывод!')

    def test5(self):
        '''
        A = {<y1, 0.7>}

        R(x) = {<<x1,y1>, 0.7>, <<x2,y1>, 0.8>}
        '''
        with open('inputs/input5.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, '<C(x1),C(x2)> ∈ ([0.7, 1.0] × [0.0, 0.7]) U ([0.0, 1.0] × 0.7) ')

    def test6(self):
        '''
        (0.3/~\C(x1))\~/(0.3/~\C(x2))\~/(0.4/~\C(x3))=0.4
        (0.5/~\C(x1))\~/(0.8/~\C(x2))\~/(0.4/~\C(x3))=0.5
        (0.1/~\C(x1))\~/(0.1/~\C(x2))\~/(0.1/~\C(x3))=0.1
        (0.7/~\C(x1))\~/(0.1/~\C(x2))\~/(0.3/~\C(x3))=0.3
        '''
        with open('inputs/input6.txt', 'r') as f:
            data = f.readlines()
        parser = Parser(data)
        parser.parse()

        for rule in parser.rules:
            for predicate in parser.predicates:
                solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
                res = solver.run()

        self.assertEqual(res, '<C(x1),C(x2),C(x3)> ∈ (0.3 × 0.5 × [0.4, 1.0]) U ([0.1, 0.3] × 0.5 × [0.4, 1.0]) U ([0.0, 0.3] × 0.5 × [0.4, 1.0]) ')
