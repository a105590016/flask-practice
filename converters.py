import typing as t
from werkzeug.routing import BaseConverter

class MyConverter(BaseConverter):
    def __init__(self, map, re):
        super().__init__(map)
        self.regex = re
        
    def to_python(self, value):
        return value
    
    def to_url(self, value):
        return value