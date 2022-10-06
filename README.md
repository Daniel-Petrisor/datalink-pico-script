# Datalink-Pico-Script

    Read data from EnviroMon System - Pico Technology and storage in sqlite3 database

## Essential hardware

    Computer - Windows system
    * EnviroMon PC application installed


    EnviroMon System - Pico Technology
    * Logger EL005
    * Converter EL041
    * Temperature Sensors


    Export data as text
    * Write the current readings to a file (see CurrentFile parameter in Envimon.ini

    If you specify a filename here, EnviroMon will write the
    current readings to a text file with this name, every
    sample interval. This can be used to transfer the data
    to another application. For example: CurrentFile=Current.txt

## Install package

    pip install pyinstaller

### Typed and Run in terminal

    * Create a one-file bundled executable.
    pyinstaller --onefile myscript.py
    pyinstaller --onefile --windowed myscript.py

    * Create a one-folder bundle containing an executable
    pyinstaller myscript.py
    pyinstaller --windowed myscript.py
