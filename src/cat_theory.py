"""
Humble beginnings of a module that encapsulates
a few functional programming and category theory concepts
"""
import sys

class Some:
    def __init__(self, x):
        self.x = x

    def contents(self):
        return self.x
    
    def __repr__(self):
        return 'Some({0})'.format(self.x)

class Nothing:
    def __init__(self, x):
        self.x = x

    def contents(self):
        return self.x
    
    def __repr__(self):
        return 'Nothing({0})'.format(self.x)

class Schema:
    def __init__(self, x):
        self.x = x
    
    def contents(self):
        return self.x
                        
    def check(self, predicate):
        if self.x != {} and self.x != [''] and predicate(self.x) == True:
            return Schema(self.x)
        else:
            return Schema({})
    
    def __repr__(self):
        return 'Schema({0})'.format(self.x)

def fold(f, acc, data):
    output = acc
    for item in data:
        output += f(acc,item)
    return output

def compose(f, g):
    apply = lambda x: f(g(x))
    return apply

def tryCatch(f, x):
    try:
        return Some(f(x))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        message = \
        '''exception type: {}
		exception object: {}
		stack trace: {}'''
        return Nothing(message.format(exc_type, exc_obj, exc_tb))