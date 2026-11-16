TASKHUB - wersja według struktury z wykładów

STRUKTURA:
- functions.py  - читання і запис даних JSON
- core.py       - основні операції завдання
- commands.py   - ком обробка
- cli.py        - режим терміналу: REPL, argparse, Click, Typer
- gui.py        - граф інтерфейс FreeSimpleGUI
- main.py       - простий файл запуск cli.py
- data/todos.json - дані прогр (створ автом.)

URUCHOMIENIE TERMINALU:
python main.py
lub
python cli.py

URUCHOMIENIE ОКРЕМОЇ КОМАНДИ:
python cli.py show
python cli.py add "Зробити лабораторну"
python cli.py done 1
python cli.py delete 1
python cli.py search лабораторну
python cli.py count
python cli.py backup

ДІАЛОГОВИЙ РЕЖИМ:
python cli.py repl

CLICK І TYper (якщо встановлені):
python cli.py click show
python cli.py typer show

ГРАФІЧНЕ ВІКНО:
python gui.py

ВСТАНОВЛЕННЯ БІБЛІОТЕК:
python -m pip install -r requirements.txt

Для CLI через argparse окремі бібліотеки не потрібні.
ПРИМІТКА:
У цій версії команда done/complete перемикає статус завдання.
Команда delete окремо видаляє завдання зі списку.
Завдання зберігаються у data/todos.json.
