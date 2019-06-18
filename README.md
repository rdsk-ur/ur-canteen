# UR Carteen Dataset

This is a dataset retrieved from the carteen's website of the University of Regensburg: https://stwno.de/de/gastronomie/speiseplan/uni-regensburg/mensa-ur

Requirements are:
+ python3
+ numpy
+ pandas
+ requests
+ jupyter (if you want to use the jupyter notebook)
+ matplotlib (if you want to use the jupyter notebook)

Run this to extend the existing dataset with more recent entries:

``` sh
python3 build_db.py
```

If you have badly formatted CSVs, fix them manually and then insert them using the python interpreter. This is how it could look like:

``` py
import build_db
build_db.insert("csv/2.csv")
```

Note that simly calling `build_db.py` wont work right now because the script checks for the latest entry and ommits any entries with a smaller date value.
