from typing import *
from pick import pick
from typing import Callable
import time

def timeit(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        starts = (
            time.time(),
            time.perf_counter(),
            time.process_time()
        )
        
        output = func(*args, **kwargs)
        
        ends = (
            time.time(),
            time.perf_counter(),
            time.process_time()
        )
        
        results = [end - start for start, end in zip(starts, ends)]
        
        print(f"[RESULTS]\nFunction Name: {func.__name__}")
        for name, value in zip(("time", "perf counter", "process time"), results):
            print(f"\t{name}: {value}")
           
        return output
    
    return wrapper 
        

# convert number to str but format number to roman
def convert_num(number : Union[float, int], type="simple") -> Union[str, int, float]:
    """
    Convierte un numero a una o otro tipo.
    type : Tipo de conversion
    number : Numero a convertir
     
    Tipos de conversion:
    simple : Convierte a simple (10000 -> 10K)
    binary : Convierte a binario (10 -> 0b1010)
    hex : Convierte a hexadecimal (10 -> 0x0A)
    """
    type = type.lower()
    try:
        number = float(number) 
    except ValueError:
        raise "F1 : El numero no es valido"
    
    if type == "simple":
        number = int(number)
        if number < 1000:
            return number
        elif number < 1000000:
            return f'{number//1000}K'
        elif number < 1000000000:
            return f'{number//1000000}M'
        else:
            return f'{number//1000000000}B'

    elif type == "binary":
        return bin(int(number))[2:]

    elif type == "hex":
        return hex(int(number))[2:]
    
    else:
        raise "F3 : Tipo de conversion no valida"
        

# creates link to put in terminal
def console_link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)


def console_pickmenu(options: List[Any], title: str, indicator:str = "->", default_index: int = 0, multiple: bool = False, min_selected: int = 0) -> Union[str, int]:

    return pick(options, title, indicator = indicator, default_index = default_index, multiselect = multiple, min_selection_count = min_selected)



