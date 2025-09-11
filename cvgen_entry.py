import sys
import argparse

def run_gui():
    from gui.main_window import MainWindow
    MainWindow().mainloop()

def run_cli():
    from core.cv_compiler import CVCompiler
    import os
    parser = argparse.ArgumentParser(description='CV Generator CLI')
    parser.add_argument('--yaml', default='resume.yaml', help='YAML input file')
    parser.add_argument('--tex', default='resume.tex', help='LaTeX output file')
    parser.add_argument('--cls', default='deedy-resume.cls', help='LaTeX class file')
    args = parser.parse_args()
    compiler = CVCompiler('build')
    success, msg = compiler.build_pipeline(args.yaml, args.tex, args.cls)
    print(msg)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    if '--cli' in sys.argv:
        run_cli()
    else:
        run_gui()
