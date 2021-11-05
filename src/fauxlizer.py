"""
Fauxlizer implementation
"""

import amyris_csv as A
import json
from math import floor
from cleanup import explode, prop
from cat_theory import compose, fold, tryCatch, Nothing, Schema

class Fauxlizer:
    def __init__(self, filename = None):
        self.filename = filename
        self.csv = A.AmyrisCsv(filename)
        self.is_valid = False
        self.has_parsed_data_file = False
        
  
    """ Fauxlizer API Methods """
    def parse_data_file(self):
        self.has_parsed_data_file = True
        return self.csv.parse_data_file(self.parse_line)
    
    
    def validate(self):
        if self.has_parsed_data_file:
            return self.is_valid
        else:
            self.parse_data_file()
            return self.is_valid
    
    
    def get_summaryBy(self, schema_key):
        """ only works for fauxness at the moment """
        if schema_key != 'fauxness': return {}
        data = self.parse_data_file()
        data_sorted = self.sortBy(schema_key, data)
        if self.is_valid:
            while True:
                if data_sorted[len(data_sorted) - 1] == {}:
                    del data_sorted[len(data_sorted) - 1]
                else:
                    break
            return \
                { 'SUMMARY': 'fauxness',
                  'SUM': self.sumBy(schema_key, data_sorted),
                  'MIN': data_sorted[0]['fauxness'],
                  'MAX': data_sorted[len(data_sorted) - 1]['fauxness']
                    }
        else:
            return {}
    
    
    def pluck_item_as_json(self, index, data):
        toJson = compose(json.dumps, prop(index))
        if index <= len(data) - 1:
            return toJson(data)
        else:
            return json.dumps({})
    
    
    """ Fauxlizer Utility Methods """
    def parse_type(self, f, d):
        maybe_type = tryCatch(f, d)
        if type(maybe_type) is Nothing:
            return False
        else:
            return True
    
    def schema_keys(self, data):
        return \
            'experiment_name' in data \
            and \
            'sample_id' in data \
            and \
            'fauxness' in data \
            and \
            'category_guess\n' in data or 'category_guess' in data 
    
    def schema_values(self, data):
        return \
            self.parse_type(lambda d: int(d[1]), data) \
            and \
            self.parse_type(lambda d: float(d[2]), data)
       
    def schema_check(self, data):
        return \
            Schema(data) \
            .check(lambda d: d is not ['']) \
            .check(lambda d: len(d) == 4) \
            .check(lambda d: self.schema_keys(self.get_headers())) \
            .check(lambda d: self.schema_values(d))
    
    def parse(self, data_invariant):
        output = {}
        if data_invariant.contents() != {}:
            data = data_invariant.contents()
            for idx, header in enumerate(self.csv.headers):
                output[header] = data[idx]
            return output
        else:
            return output
    
    def parse_line(self, line):
        """ ex. {experiment_name: 'examination.76377',
                sample_id: 449491,
                fauxness: 0.651592972723,
                category_guess: fake} """
        data = explode(line, ',')
        result = compose(self.parse, self.schema_check)(data)
        if result != {}: self.is_valid = True
        return result

    
    def get_headers(self):
       return self.csv.headers
       
    
    def sumBy(self, schema_key, data):
        """ only works for fauxness at the moment """
        fauxness = compose(float, prop(schema_key))
        reducer = lambda acc,x: acc + fauxness(x)
        return fold(reducer, 0.0, data)
    
    
    def sortBy(self, key, lst):
        """ merge sort on the schema key's value"""
        if len(lst) < 2: return lst
        mid = floor(len(lst) / 2)
        left = self.sortBy(key, lst[mid:])
        right = self.sortBy(key, lst[:mid])
        
        # merge
        i = j = 0
        sortedlist = [ ]

        obj_prop = compose(float, prop(key))
        
        while len(sortedlist) < len(lst):
            if j >= len(right) or i < len(left) and left[i] != {} and right[j] != {} and obj_prop(left[i]) < obj_prop(right[j]):
                sortedlist.append(left[i])
                i += 1
            elif j < len(right):
                sortedlist.append(right[j])
                j += 1
                
        return sortedlist
    
    
""" Test Runner """
def main(fauxlizer_file):
    f = Fauxlizer(fauxlizer_file)
    # parse
    data = f.parse_data_file()
    print('Fauxlizer run for data file: {0} \n'.format(fauxlizer_file))
    print(data)
    print('\n')
    # validate
    print('Is data file valid: {0} \n'.format(f.validate()))
    # summary
    print(f.get_summaryBy('fauxness'))
    print('\n')
    # retrieve row by alternate format, i.e. JSON
    print(f.pluck_item_as_json(0, data))


if __name__ == '__main__':
    main('././data_files/file_1.faux') # valid test run
    print('\n')
    main('././data_files/file_3.faux') # invalid test run 