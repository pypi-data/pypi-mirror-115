# directory-structure

Print a directory tree structure in your Python code.

## Download

You can simply:

```sh
pip install directory-structure
```

Or you can also:

1. Clone the repository to your local machine.
2. Enter the directory.
3. Download necessary modules/libraries.

```sh
git clone https://github.com/gabrielstork/directory-structure.git
cd directory-structure
pip install -r requirements.txt
```

## Examples

`complete=True`:

```python
from directory_structure.tree import Tree

path = Tree('C:/Users/User/Desktop/directory-structure', complete=True)
print(path)
```

```text
📂 C:
|_📂 Users
  |_📂 User
    |_📂 Desktop
      |_📂 directory-structure
        |_📁 .git
        |_📁 dist
        |_📁 src
        |_📁 tests
        |_📄 LICENSE
        |_📄 pyproject.toml
        |_📄 README.md
        |_📄 requirements.txt
        |_📄 setup.py
```

`complete=False`:

```python
from directory_structure.tree import Tree

path = Tree('C:/Users/User/Desktop/directory-structure', complete=False)
print(path)
```

```text
📂 directory-structure
|_📁 .git
|_📁 dist
|_📁 src
|_📁 tests
|_📄 LICENSE
|_📄 pyproject.toml
|_📄 README.md
|_📄 requirements.txt
|_📄 setup.py
```
