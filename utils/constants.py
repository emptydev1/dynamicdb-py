import os

operators = [ "+", "-", "*", "/", "%" ]
default_config = {
  "path": os.path.abspath(os.path.join("databases", "database.json")),
  "max_data_size": None
}
version = "1.0.0"
constants = {
  "default_config": default_config, 
  "version": version
}
