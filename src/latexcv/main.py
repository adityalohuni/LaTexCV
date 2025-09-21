import sys
import argparse

def run_gui():
    from gui.main_window import MainWindow
    MainWindow().mainloop()

def run_cli():
    from cli import run_cli
    run_cli()

def main():
    if len(sys.argv)>1:
        run_cli()
    else:
        run_gui()
