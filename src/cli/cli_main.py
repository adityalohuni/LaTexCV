"""
CLI entry point for LaTexCV project (moved to src/cli/cli_main.py).
"""
import argparse
import sys
import os
from src.core.cv_compiler import CVCompiler
from src.core.generator.resume_generator import ResumeGenerator

def run_cli():
    parser = argparse.ArgumentParser(description="LaTexCV CLI - Compile and generate resumes from YAML.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Compile CV command
    compile_parser = subparsers.add_parser("compile", help="Compile CV from YAML file.")
    compile_parser.add_argument("yaml_file", type=str, help="Path to the resume YAML file.")
    compile_parser.add_argument("--output", type=str, default="resume.pdf", help="Output PDF filename.")

    # Generate resume command
    generate_parser = subparsers.add_parser("generate", help="Generate resume from YAML.")
    generate_parser.add_argument("yaml_file", type=str, help="Path to the resume YAML file.")
    generate_parser.add_argument("--template", type=str, default="deedy", help="LaTeX template to use.")
    generate_parser.add_argument("--output", type=str, default="resume.tex", help="Output LaTeX filename.")

    args = parser.parse_args()

    if args.command == "compile":
        cls_file = os.path.join("cls", "deedy.cls")
        compiler = CVCompiler("build")
        success, msg = compiler.build_pipeline(args.yaml_file, args.output.replace(".pdf", ".tex"), cls_file)
        print(msg)
        sys.exit(0 if success else 1)
    elif args.command == "generate":
        cls_file = os.path.join("cls", f"{args.template}.cls")
        generator = ResumeGenerator(args.yaml_file, cls_file)
        try:
            generator.generate(args.output)
            print(f"LaTeX resume generated: {args.output}")
        except Exception as e:
            print(f"Error generating resume: {e}")
            sys.exit(1)
    else:
        parser.print_help()


