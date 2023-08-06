from .file_pack import *
from .sqllite_orm_pack import *

if __name__ == '__main__':
    # Защита чтобы ide не убирал импорт
    print(debugger.Debugger.AllActiveInstance)
