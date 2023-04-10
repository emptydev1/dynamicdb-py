# DynamicDB

<p>A JSON database made in Python simple and easy to use.</p>

# About the Database

- Simple to use and has many functions
- Developed using Python

---
# Cloning this repo
```sh-session
git clone https://github.com/emptydev1/dynamicdb.py
cd dynamicdb.py
```

---
# Setup

<p>Create a file called `requirements.txt` in your project and copy this:</p>

```txt
git+https://github.com/emptydev1/dynamicdb.py.git
```

<p>After doing so, you must run the following command:</p>

```sh-session
pip install -r requirements.txt
```

---
# How to use the Database?

<p>Here below are some simple examples of how you can utilize this database:</p>

```py
# Importing the database
from dynamicdb import Database

# Creating a new instance
db = Database({
  "path": "path/to/your/database",
  "max_data_size": 200 # Default is "None"
})

# Entering (or changing) a value
db.insert("key", "Hello, world!")
db.insert("number", 500)
db.insert("user_one", {
  "name": "John",
  "age": 27,
  "hobbies": [ "play", "program" ]
})
db.insert("user_two", {
  "name": "Leonard",
  "age": 23,
  "hobbies": [ "study", "play", "walk around" ]
})

# Get a value
db.get("key") # Output: Hello, world!
db.get("number") # Output: 500

# Fetch a value
db.fetch("name", "John Doe") # This method returns a value if it already exists, otherwise it will insert a new value in the database

# Add a value
db.add("number", 500) # 1000

# Subtract a value
db.sub("number", 500) # 500

# Multiply a value
db.multi("number", 4) # 2000

# Divide a value
db.divide("number", 4) # 500

# Math method (operators: +, -, *, /, %)
db.math("number", "%", 3) # 2

# Delete a value
db.delete("key")

# Get all values
db.all()

# Get the database size
db.size

# Copying this database to another path
db.copy({
  "path": "path/to/new/database"
})

# Mapping database values
db.map(lambda el: type(el["value"]))

# Filtering database values
db.filter(lambda el: el["key"].startswith("user_"))

# See the type of a value
db.type("number") // <class 'int'>

# Convert database values to a JSON
db.toJSON()

# Checks if a value exists
db.exists("key") # False
db.has("number") # True

# An array with all database keys
db.keys()

# An array with all database values
db.values()

# Get the database ping in ms
db.ping()

# Clear the database
db.clear()

# Unlink the database path
db.unlink()
```

<p>These are just some of the functionalities that this database has. If you want to know more about it, join our Discord server!</p>

# Links

- **[Discord Server](https://discord.com)**
- **[Github Repository](https://github.com/emptydev1/dynamicdb.py)**
- **[Github Creator's Profile](https://github.com/emptydev1)**

# Contributors

- **[Empty™#4646 (emptydev1)](https://discord.com/users/1036018691562803260)**
