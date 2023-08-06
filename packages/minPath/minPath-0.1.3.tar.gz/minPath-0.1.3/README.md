# minPath
a file system simulation

# installation

Run the following to install:
```cmd
pip install minPath
```
### or
```cmd
python -m pip install minPath
```
if that didn't work, try replacing `pip` with `pip3`.

need help? or have bugs to report, let me know in the [lab](https://discord.gg/vzEZnC7CM8)

# getting started
```python
from minPath import *

my_files = [File("hay.py","print('Hello, World!')"),File("Hi.py","print('Hi')"),File("text.txt","here a text file"),File("BRUH",None),Folder("test",[File("testing.txt","A test file for my MiniPath testing"),File("huh.txt","anther testing file"),Folder("Folder 2"),Folder("empty",[File("empty file","nothing here :("),Folder("o")])]),File("random")]

pa = MiniPath("C:",my_files,path_sep="\\")
print(str(pa))
print(dir(pa)) # dir attrs
#help(File); help(Folder)


"""
# dump
with open("minPath.pickle","wb") as file:
	pickle.dump(pa)
"""

```


File class is file-like object
Folder is Folder_Array


if you needed **help** join the [lab](https://discord.gg/vzEZnC7CM8)


## pickling, unpickling
how to dump and load minpath object
```python
import pickle
from minPath import *

# load
with open("minPath.pickle","rb") as file:
	pa = pickle.load(file)

# do stuff
...

# dump
with open("minPath.pickle","wb") as file:
	pickle.dump(pa)

```
> Warning do not edit the file this may break the file

