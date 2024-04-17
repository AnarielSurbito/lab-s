from typing import List

def read_file(file_name : str = '.\\tests\\1' ) -> List[str]:
    data : List[str] = []
    with open(file=file_name) as f:
        for line in f:
            data.append(line.strip('\n'))
    return data
