from __future__ import annotations
import sys, csv
from pathlib import Path
from io import IOBase
from tabulate import tabulate
from .format import get_default_csv_dialect_name


class Flexout:
    """
    ## Usage examples
    
    ### Export text either on stdout or on csv file

    ```
    with Flexout(filename or "stdout") as o:
        o.file.write("10: Zidane")
    ```
    
    ### Export tabular data either on stdout or on csv file

    ```
    with Flexout(filename or "stdout") as o:
        o.append_headers("Id", "Name")
        o.append_row(10, "Zidane")
    ```
    """
    file: IOBase

    def __init__(self, out: str|Path|IOBase = None, append: bool = False, newline: str = None, encoding: str = None, csv_dialect: str = None, **kwargs):
        self._append = append
        self._newline = newline
        self._encoding = encoding
        self._csv_dialect = csv_dialect

        # Update out
        self._file_opened = False
        self.file: IOBase = None
        self._strpath: str = None
        if out == False or out == "noop":
            pass # noop
        else:
            if not out or out == "stdout":
                self.file = sys.stdout
            elif out == "stderr":
                self.file = sys.stderr
            elif isinstance(out, IOBase):
                self.file = out
            elif isinstance(out, Path):
                self._strpath = str(out)
            elif isinstance(out, str):
                self._strpath = out
            else:
                raise ValueError(f"invalid type for argument \"out\": {type(out).__name__}")

        # For CSV file:
        # - Set newline to '', otherwise newlines embedded inside quoted fields will not be interpreted correctly. See footnote of: https://docs.python.org/3/library/csv.html
        # - Set encoding to utf-8-sig (UTF8 with BOM): CSV is for exchanges, encoding should not depend on the exporting operating system. BOM is necessary for correct display with Excel
        if (self._strpath and self._strpath.lower().endswith(".csv")) or self._csv_dialect:
            if self._newline is None:
                self._newline = ''
            if self._encoding is None:
                self._encoding = 'utf-8-sig'

        # Handle strpath
        if self._strpath:
            # Replace "{key}" in path by keyword arguments
            for key, value in kwargs.items():
                self._strpath = self._strpath.replace("{"+key+"}", value)
        elif self.file:
            if hasattr(self.file, "name"):
                self._strpath = self.file.name
            if not self._strpath:
                self._strpath = f"<{type(self.file).__name__}>"

    def __enter__(self):
        if not self.file and self._strpath:
            self._file_opened = True
            Path(self._strpath).parent.mkdir(parents=True, exist_ok=True)
            self.file = open(self._strpath, "a" if self._append else "w", newline=self._newline, encoding=self._encoding)
        return self

    def __exit__(self, *args):
        if not self.file and not self._strpath:
            return # noop
        
        if self._file_opened:
            # CSV to file
            if self.headers:
                self.csv_writer.writerow(self.headers)
            
            if self.rows:
                for row in self.rows:
                    while len(row) < len(self.headers):
                        row.append(None)
                    self.csv_writer.writerow(row)

            self.file.close()
        
        else:
            # Tabulate to IOBase
            if self.headers or self.rows:
                print(tabulate(self.rows, headers=self.headers), file=self.file)

    def __str__(self) -> str:
        if self._strpath:
            return self._strpath
        else:
            return "<noop>"

    # -------------------------------------------------------------------------
    # For tabular data
    # -------------------------------------------------------------------------

    @property
    def headers(self):
        if not hasattr(self, "_headers"):
            return None
        return self._headers
    
    def append_headers(self, *args):
        headers = args[0] if len(args) == 1 and isinstance(args[0], list) else args
        if hasattr(self, "_headers"):
            self._headers += headers
        else:
            self._headers = headers

    @property
    def rows(self) -> list[list]:
        if not hasattr(self, "_rows"):
            self._rows = []
        return self._rows

    def append_row(self, *args):
        if not self.file and not self._strpath:
            # noop
            return
        
        if len(args) == 1 and isinstance(args[0], dict):
            # input contains header and value
            if not hasattr(self, "_headers"):
                self._headers = []
            
            row = [None] * len(self._headers)
            
            for header, value in args[0].items():
                try:
                    index = self._headers.index(header)
                    row[index] = value
                except:
                    self._headers.append(header)
                    row.append(value)

        elif len(args) == 1 and isinstance(args[0], list):
            row = args[0]
        else:
            row = args

        self.rows.append(row)

    @property
    def csv_writer(self):
        if not hasattr(self, "_csv_writer"):
            dialect = get_default_csv_dialect_name()
            self._csv_writer = csv.writer(self.file, dialect=dialect)
        return self._csv_writer
