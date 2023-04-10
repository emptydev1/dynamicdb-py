from src.utils.constants import operators, default_config
from datetime import datetime
import tempfile
import shutil
import random
import json
import os 

class Database:
    def __init__(self, options = {}):
        if not isinstance(options, dict):
            raise TypeError(f"The 'options' object must be of type dict, received: {type(options)}")
        if "path" not in options:
            options["path"] = default_config["path"]
        elif not isinstance(options["path"], str):
            options["path"] = default_config["path"]
        if "max_data_size" not in options:
            options["max_data_size"] = default_config["max_data_size"]
        if options["max_data_size"] is not None and not isinstance(options["max_data_size"], int):
            raise TypeError(f"Parameter 'max_data_size' must be of type int, received: {type(options['max_data_size'])}")
        if options["max_data_size"] is not None and options["max_data_size"] <= 1:
            raise ValueError("Parameter 'max_data_size' must be greater than 1")
        if options["path"].startswith(f".{os.sep}"):
            options["path"] = options["path"][2:]
        if options["path"].startswith(os.getcwd()):
            options["path"] = options["path"][len(os.getcwd()) + 1:]
        if not options["path"].endswith(".json"):
            if options["path"].endswith(os.sep):
                options["path"] += "database.json"
            else:
                options["path"] += ".json"
        
        dirs = options["path"].split(os.sep)
        options["path"] = os.path.abspath(options["path"])
        
        if len(dirs) > 1:
            dirs.pop();
            
            target = os.path.abspath(dirs[0]);
            
            if not os.path.exists(target):
                os.mkdir(target);
            dirs.pop(0);
            
            for dir in dirs:
                current = os.path.join(target, dir);
                if not os.path.exists(current):
                    os.mkdir(current);
                target += os.sep + current;
            
        if not os.path.exists(options["path"]):
            with open(options["path"], "w") as file:
                json.dump([], file);
            
        self.path = options["path"];
        self.max_data_size = options["max_data_size"];
        self._utm = int(datetime.now().timestamp() * 1000);
    
    @property
    def size(self):
        return len(self.all());
    
    def insert(self, key, value):
        index = self.find_index(lambda el: el["key"] == key);
        data = self.all();
        
        if not isinstance(key, str):
            raise TypeError(f"Paramter 'key' must be of type str, received: {type(key)}");
        if self.max_data_size is not None and self.size >= self.max_data_size:
            raise OSError("The max data size of this database has been exceeded");
        
        if index >= 0:
            data[index] = { "key": key, "value": value };
        else:
            data.append({ "key": key, "value": value });
        
        self.write(data);
        return value;
    
    def set(self, key, value):
        return self.insert(key, value);
    
    def get(self, key, df = None):
        found = self.find(lambda el: el["key"] == key, df);
        
        return found["value"] if found else df;
    
    def delete(self, key):
        data = self.all();
        index = self.find_index(lambda el: el["key"] == key);
        
        if not isinstance(key, str):
            raise TypeError(f"Parameter 'key' must be of type str, received: {type(key)}");
        
        if index >= 0:
            del data[index];
            self.write(data);
            return True;
        else:
            return False;
    
    def fetch(self, key, value):
        return self.get(key) if self.exists(key) else self.insert(key, value);
    
    def type(self, key):
        return type(self.get(key)) if self.exists(key) else None;
   
    def all(self, limit = 0):
        if not isinstance(limit, int):
           raise TypeError(f"Paramter limit must be of type int, received: {type(limit)}");
        
        with open(self.path, "r") as file:
            data = json.load(file);
            
            return data[:limit] if limit > 0 else data;
     
    def toJSON(self, limit = 0):
        data = self.all();
        obj = {};
        
        for item in data:
            obj[item["key"]] = item["value"];
            
        return obj;
    
    def entries(self, limit = 0):
        data = self.all(limit);
        arr = [];
        
        for item in data:
            arr.append([ item["key"], item["value"] ]);
          
        return arr;
   
    def stringify(self, limit = 0):
        return json.dumps(self.all(limit));
    
    def math(self, key, operator, value):
        data = self.get(key);
        
        if type(value) is not int:
            raise TypeError(f"Paramter 'value' must be of type int, received: {type(value)}");
        if type(data) is not int:
            raise TypeError(f"Value of key '{key}' is not of type int");
            
        if operator == "+":
            data += value;
        elif operator == "-":
            data -= value;
        elif operator == "*":
            data *= value;
        elif operator == "/":
            data /= value;
        elif operator == "%":
            data %= value;
        else:
            raise TypeError(f"The '{operator}' operator is not a valid operator, must be one of: {', '.join(operators)}");
            
        return self.insert(key, int(data));
    
    def sum(self, key, value):
        return self.math(key, "+", value);
    
    def sub(self, key, value):
        return self.math(key, "-", value);
    
    def divide(self, key, value):
        return self.math(key, "/", value);
    
    def multi(self, key, value):
        return self.math(key, "*", value);
    
    def exists(self, key):
        return key in self.keys();
    
    def has(self, key):
        return self.exists(key);
    
    def keys(self):
        return self.map(lambda el: el["key"]);
    
    def values(self):
        return self.map(lambda el: el["value"]);
    
    def map(self, callback):
        return list(map(callback, self.all()));
    
    def filter(self, callback):
        return list(filter(callback, self.all()));
    
    def find_index(self, callback):
        data = self.filter(callback);
        
        return self.all().index(data[0]) if len(data) > 0 else -1;
        
    def find(self, callback, df = None):
        return next(filter(callback, self.all()), df);
    
    def clear(self):
        self.write([]);
        return [];
    
    def unlink(self):
        os.remove(self.path);
    
    def write(self, data):
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as tmp_file:
            json.dump(data, tmp_file);
            tmp_file.flush();
            os.fsync(tmp_file.fileno());
            shutil.move(tmp_file.name, self.path);
     
    def copy(self, options, limit = 0):
        data = self.all(limit)
        
        if "max_data_size" not in options:
            options["max_data_size"] = default_config.max_data_size;
        if "path" not in options:
            raise TypeError("Missing option \"path\"");
        if options["max_data_size"] and len(data) > options["max_data_size"]:
            raise OSError(f"The amount of data that would be copied exceeds the maximum data size that has provided in options [{len(data)}/{options.max_data_size}]");
        
        copy = Database(options);
        
        for item in data:
            copy.insert(item["key"], item["value"]);
        
        return copy;
     
    def find_and_delete(self, callback):
        if not callable(callback) and not hasattr(callback, "__call__"):
            raise TypeError(f"Parameter 'callback' must be of type function, received: {type(callback)}");
        
        data = self.filter(callback);
        size = 0;
         
        for item in data:
            self.delete(item["key"]);
            size += 1;
         
        return size;
     
    def for_each(self, callback):
        if not callable(callback) and not hasattr(callback, "__call__"):
            raise TypeError(f"Parameter 'callback' must be of type function, received: {type(callback)}");
        
        for item in self.all():
            callback(item);
     
    def pop(self):
        data = self.all();
        output = data.pop();
        
        self.write(data);
        return output;
     
    def shift(self):
        data = self.all();
        output = data.pop(0);
        
        self.write(data);
        return output;
     
    def at(self, index, df = None):
        if not isinstance(index, int):
            raise TypeError(f"Parameter 'index' must be of type int, received: {type(index)}");
        
        return self.all()[index] if self.size >= index else df;
     
    def random(self, callback = None):
        if callback is not None and not callable(callback) and not hasattr(callback, "__call__"):
            raise TypeError(f"Parameter 'callback' must be of type function, received: {type(callback)}");
        
        data = self.filter(callback) if callback is not None else self.all();
        index = random.randint(0, len(data) - 1);
        
        return data[index];
    
    def reverse(self):
        data = self.all();
        data.reverse();
        return data;
    
    def first(self):
        return self.all()[0];
    
    def last(self):
        return self.all()[self.size - 1];
    
    def ping(self):
        start = datetime.now().timestamp() * 1000;
        self.all();
        return int((datetime.now().timestamp() * 1000) - start);






