'''
Лабораторная работа №2 по дисциплине ЛОИС
Выполнена студентами группы 121703 БГУИР Юрченко В. Ф., Шелк П. С.
Вариант 6: нечеткая композиция (max({min({x_i} U {y_i}) | i})
Задача: разработать программу, выполняющую обратный нечеткий логический вывод
'''
import re


class Parser:
    def __init__(self, data):
        self.data = data
        self.predicates = []
        self.rules = []

    def delete_spaces(self):
        """Удаляет пробельные символы в self.data"""
        self.data = [item.replace(' ', '').replace('\n', '') for item in self.data]

    def parse_data(self):
        """
        Разбивает self.data на предикаты и правила
        """

        rules_index = self.data.index('')
        self.predicates.extend(self.data[:rules_index])
        self.rules.extend(self.data[rules_index + 1:])

    @staticmethod
    def parse_rule_string(rule_string: str):
        rule_match = re.match(r'R\((\w+)\)={(.+)}', rule_string)

        if rule_match:
            rule_name = rule_string.split('=')[0]
            set_string = rule_match.group(2)

            set_entries = re.findall(r'<<([^>]+)>,(\d+\.\d+)>', set_string)

            rule = {
                'name': rule_name,
                'set': {f'{entry[0]}': float(entry[1]) for entry in set_entries}
            }

            return rule
        else:
            raise ValueError('Invalid rule string format')

    def validate_predicates(self):
        reg_exp = r"([A-Z]\d*)=(\{(\<[a-z]\d*,\d(\.\d+)?\>)(,\<[a-z]\d*,\d(\.\d+)?\>)*})|\{\}"
        for item in self.predicates:
            if item != '' and not re.match(reg_exp, item):
                raise RuntimeError('invalid input format')

    @staticmethod
    def parse_set(sets: list) -> list[dict]:
        """
        приводит нечеткие множества set в список с элементами формата:
        {'name': 'A', 'set': {'x1': 0.1, 'x2': 0,2}}
        """
        parsed = []
        for item in sets:
            splited = item.split('=')
            set_values: list[str] = splited[1].replace('{', '').replace('}', '').split('>,')
            data = {'name': splited[0],
                    'set':
                        {
                            item.split(',')[0].replace('<', ''):
                                float(item.split(',')[1].replace('>', ''))
                            for item in set_values
                        }
                    }
            if len(data.get('set')) != len(set_values):
                print(
                    f'Внимание! Множество {item} содержит элементы с одинаковым названием, сохранено будет только последнее вхождение этого элемента')
            parsed.append(data)
        return parsed

    @staticmethod
    def format_rule(rule):
        """Для вывода правила в консоль"""
        name = rule['name']
        set_entries = ', '.join([f'<<{key}>, {value}>' for key, value in rule['set'].items()])

        formatted_rule = f'{name} = {{{set_entries}}}'

        return formatted_rule

    @staticmethod
    def format_set(set: dict):
        """Для вывода предиката в консоль"""
        output = f"{set['name']} = " + '{'
        for var, val in set['set'].items():
            output += f'<{var}, {val}>, '
        return output.removesuffix(', ') + '}'

    def parse(self):
        self.delete_spaces()
        self.parse_data()
        self.validate_predicates()
        self.predicates = self.parse_set(self.predicates)
        parsed_rules = []
        for rule in self.rules:
            parsed_rules.append(self.parse_rule_string(rule))

        self.rules = parsed_rules
