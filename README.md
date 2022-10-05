* Datalink-Pico-Script
    Read data from logger EL005 - Pico Technology and storage in sqlite3 database




** CREATE APP.EXE
* Install package

    pip install pyinstaller

* The syntax of the pyinstaller command is:

    pyinstaller [options] script [script …] | specfile


* Typed and Run in terminal

    - Create a one-file bundled executable.
    pyinstaller nome_script.py --onefile
    pyinstaller nome_script.py --noconsole --onefile
    pyinstaller --onefile --windowed myscript.py
  
    - Create a one-folder bundle containing an executable
    pyinstaller myscript.py
    pyinstaller --windowed myscript.py
    