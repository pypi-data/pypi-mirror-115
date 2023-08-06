import os

__all__ = []
__files__ = os.listdir(".")

for file in __files__:
    ext = os.path.splitext(file)[-1]
    name = os.path.splitext(file)[0]

    if ext == ".py" and name != "__init__":
        __all__.append(name)
