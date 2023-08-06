# InMemDB: powered by sqlite

## What it is?

InMemDB is a Python package that combines sqlalchemy and pandas to easily create GUI-less in memory sqlite relational databases.

## Main Features

Here are a few things that InMemDB does well:

- Create relational databases in RAM, offering quick speed
- Returns a pandas DataFrame allowing for the use all associated panda methods
- Tables can be created from pandas DataFrames, lists, and dictionaries

## Advantages

- Combines SQLilte with the best data manipulation and analysis tool Pandas
- Can be used to Extract, Transform, and Load data
- Those who are more familar with SQL can still manipulate the powerful pandas DataFrame seamlessly

## Usage:

```python
from inmemdb.InMemDB import InMemDB
db = InMemDB()
db.createTableFromDF(tableName='table_name',df=pandas.DataFrame)
```

## Demo:

- https://github.com/kwe92/InMemDB-Demo/blob/main/inmemdb_demo.ipynb