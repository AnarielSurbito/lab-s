'''
Лабораторная работа №2 по дисциплине ЛОИС
Выполнена студентами группы 121703 БГУИР Юрченко В. Ф., Шелк П. С.
Вариант 6: нечеткая композиция (max({min({x_i} U {y_i}) | i})
Задача: разработать программу, выполняющую обратный нечеткий логический вывод
'''
from itertools import product


class InverseFuzzyInference:
    def __init__(self, logical_conclusion: dict, rule: dict):
        self.logical_conclusion = logical_conclusion
        self.rule = rule
        self.equations = []
        self.varnames = {self.get_first_var_name(key) for key in rule['set'].keys()}

    def run(self):
        # составляем систему уравнений
        self.make_equations()
        solutions = []

        # решаем каждое уравнение
        for eq in self.equations:
            solutions.append(self.solve_equation(eq))

        # ищем пересечения
        permutations = list(product(*solutions))

        result_intersections = []
        for solution in permutations:
            result = self.find_intersection(solution)
            if result and result not in result_intersections:
                result_intersections.append(result)


        if len(result_intersections) == 0:
            res = 'Нельзя построить обратный вывод!'
            print(res)
            return res

        print('Результатом обратного вывода будет предикат С такой, что')
        return self.print_result(result_intersections)

    def find_intersection(self, solutions):
        # solution ({'x1': (0.1, 0.3), 'x2': (0.0, 1.0)},
        # {'x1': (0.1, 0.2), 'x2': (0.0, 1.0)},
        # {'x1': (0.3, 0.3), 'x2': (0.0, 1.0)})

        intersections = []
        for varname in sorted(self.varnames):
            varname_intervals = [solution[varname] for solution in solutions if solution.get(varname)]
            if len(varname_intervals) == 0:
                raise RuntimeError('Пересечений нет!')

            intersection = {varname: (
                max(interval[0] for interval in varname_intervals),
                min(interval[1] for interval in varname_intervals))
            }

            if any(value[0] > value[1] for value in intersection.values()):
                return None

            intersections.append(intersection)

        return intersections


    def make_equations(self):
        """Создает систему уравнений на основе правила и множества следствий"""
        for name, value in self.logical_conclusion['set'].items():
            equation = {'right_part': value}
            left_part = []
            for name1, value1 in self.rule['set'].items():
                if self.get_second_var_name(name1) == name:
                    min_set = (value1, self.get_first_var_name(name1))
                    left_part.append(min_set)

            equation['left_part'] = left_part
            self.equations.append(equation)

        return None

    @staticmethod
    def solve_equation(equation):
        """решает уравнение логическим методом"""
        solutions = []
        var_names = [varname[1] for varname in equation['left_part']]

        for min_set in equation['left_part']:

            # min_set (0.1, 'x1')
            solution = {}  # solution {'x1': (0.1, 1.0)}
            if min_set[0] == equation['right_part']:
                solution = {
                    min_set[1]: (min_set[0], 1.0),
                }
            elif min_set[0] < equation['right_part']:
                continue
            elif min_set[0] > equation['right_part']:
                solution = {
                    min_set[1]: (equation['right_part'], equation['right_part'])
                }

            for other_min_set in equation['left_part']:
                if other_min_set == min_set:
                    continue

                if other_min_set[0] > equation['right_part']:
                    solution.update({
                        other_min_set[1]: (0.0, equation['right_part'])
                    })
                else:
                    solution.update({
                        other_min_set[1]: (0.0, 1.0)
                    })

            solutions.append(solution)

        return solutions

    @staticmethod
    def get_second_var_name(elem_name: str):
        return elem_name.split(',')[1]

    @staticmethod
    def get_first_var_name(elem_name: str):
        return elem_name.split(',')[0]

    def print_result(self, result):
        repr = '<'
        for var in sorted(self.varnames):
            repr += f'C({var}),'
        repr = repr.removesuffix(',') + '> ∈ '
        for res in result:
            repr += '('
            for value in res:
                for value in value.values():
                    left, right = value
                if left == right:
                    repr += f'{left} × '
                else:
                    repr += f'{[left, right]} × '
            repr = repr.removesuffix(' × ') + ') U '

        repr = repr.removesuffix('U ')

        print(repr, end='\n\n')

        return repr


# if __name__ == '__main__':
#     rule = {
#         'name': 'R',
#         'set': {
#             'x1,y1': 0.7,
#             'x1,y2': 0.1,
#             'x1,y3': 0.2,
#             'x2,y1': 0.7,
#             'x2,y2': 0.3,
#             'x2,y3': 0.1,
#         }
#     }
#     logical_conclusion = {
#         'name': 'A',
#         'set': {
#             'y1': 0.7,
#             'y2': 0.3,
#             'y3': 0.2
#         }
#     }
#     rule = {
#         'name': 'R',
#         'set': {
#             'x1,y1': 0.7,
#             'x1,y2': 0.1,
#             'x1,y3': 0.1,
#             'x2,y1': 0.5,
#             'x2,y2': 0.1,
#             'x2,y3': 0.1,
#         }
#     }
#     logical_conclusion = {
#         'name': 'A',
#         'set': {
#             'y1': 0.6,
#             'y2': 0.2,
#             'y3': 0.2
#         }
#     }
#     rule = {
#         'name': 'R',
#         'set': {
#             'x1,y1': 0.7,
#             'x1,y2': 0.8,
#             'x1,y3': 0.3,
#             'x2,y1': 0.7,
#             'x2,y2': 0.8,
#             'x2,y3': 0.3,
#         }
#     }
#     logical_conclusion = {
#         'name': 'A',
#         'set': {
#             'y1': 0.7,
#             'y2': 0.8,
#             'y3': 0.3
#         }
#     }
#     solver = Solver(logical_conclusion, rule)
#     solver.run()
