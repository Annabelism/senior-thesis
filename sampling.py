import random
from MBFC import data

def save_and_write(data):
    sampled_dicts = random.sample(data, 100)

    output_python_file = 'data100.py'

    with open(output_python_file, mode='w', encoding='utf-8') as pyfile:
        pyfile.write('data = [\n')  
        for d in sampled_dicts:
            dict_string = repr(d)
            pyfile.write('    ' + dict_string + ',\n')
        pyfile.write(']\n')  # End the list

save_and_write(data)