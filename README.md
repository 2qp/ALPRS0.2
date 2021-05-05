# ALPRS

Forked from  : 

https://gist.github.com/jkjung-avt/790a1410b91c170187f8dbdb8cc698c8

which is dedicated to nvidia jetson hardwares.
----------------------------------------------------------------------------

Changes :

compatibility to AMD64 x86_x64

Simple GTK GUI

output of plate extraction.
check allowed number plates using SQLite3

triggering arduino uno board upon allowed number plates.

----------------------------------------------------------------------------
fully compatible with debian buster

Compatible Libs

- Python 2.7.3
- OpenCV 4.0
- Leptonica 1.80.0
- Tesseract-ocr 3.04
- OPENALPR

----------------------------------------------------------------------------
Other Third-party Libs

- GTK MVC Framework for SQlite3 : https://github.com/nowsecure/datagrid-gtk3
- Cairo

```sh
sudo apt-get install python-gi-cairo
pip install pycairo==1.16.2

```

----------------------------------------------------------------------------

Using SQLite3 PySQL

create a local db using sqlite and specify the path

Connect DB in script.py
```sh
conn = sqlite3.connect('stu3.db')
c = conn.cursor()
```

Specify DB Path and Tables in allowed.py

```sh

path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
db_path = os.path.join(path, 'stu3.db')

data_source = SQLiteDataSource(
    db_path, 'stu3', ensure_selected_column=True)

```
