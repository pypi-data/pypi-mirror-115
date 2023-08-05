from functools import wraps
import json

def parse(file_name, path):
    path = path.split(".")
    def decorator(klass):
        old_init = klass.__init__
        @wraps(klass.__init__)
        def decorated_init(self):
            with open(file_name, "r") as inputFile:
                config_data = json.loads(inputFile.read())
                for x in path:
                    config_data = config_data[x]
                old_init(self,**config_data)
        klass.__init__ = decorated_init
        return klass
    return decorator