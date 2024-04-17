import file_reader
import re
from typing import List

class InputError(Exception):
    def __init__(self, *args: object) -> None:
        self.__message = args[0]
    def __str__(self) -> str:
        return self.__message

def is_valid(data: List[str]) -> List[str]:
    sets = []
    functions = []
    for item in data:
        if re.findall(r"[a-z]\([a-z]\) = {(\([a-z], \d(\.\d)?\), )*(\([a-z], \d(\.\d)?\))?}",item) != []:
            sets.append(item)
        elif re.findall(r'[a-z]\([a-z], [a-z]\) = \([a-z]\([a-z]\) ~> [a-z]\([a-z]\)\)',item) != []:
            functions.append(item)
    if sets == []:
        raise InputError('No sets were defined')
    if functions == []:
        raise InputError('No functions were defined')
    return sets,functions
    
def parsing(iteration : int = 0):
    file_data = file_reader.read_file(f".\\tests\\{iteration+1}")
    sets, functions = is_valid(file_data)
    data = {
        'values' : [],
        'functions' : []
    }
    for item in sets:
        key = item[:item.index('(')]
        item = item[item.index('{'):]
        item = item.replace("{", "").replace("}", "")
        if len(item) == 0:
            values = {}
        else:
            item = item.split('), (')
            item = [x.replace('(','').replace(')','') for x in item]
            values = {key:value for element in item for key,value in [element.split(', ')] }
        dict_values = {
            key:values
        }
        data['values'].append(dict_values)
    for item in functions:
        key = item[:item.index('(')]
        item = item[item.index('= (')+3:][:-1]
        key = [x[:x.index('(')] for x in item.split(' ~> ')]
        data['functions'].append(key)
    return data


