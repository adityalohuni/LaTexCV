import yaml
from pathlib import Path
import os


def latex_header(data):
    cls_file = data.get('cls', None)
    if not cls_file:
        cls_file = 'template.cls'
    cls_path = Path(cls_file)
    cls_name = cls_path.stem
    return [
        r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
        r'% Auto-generated from resume.yaml',
        r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
        rf'\documentclass[]{{{cls_name}}}',
        r'\usepackage{fancyhdr}',
        r'\usepackage{hyperref}',
        r'\usepackage{fontawesome}',
        r'\usepackage[usenames,dvipsnames]{xcolor}',
        r'\pagestyle{fancy}',
        r'\fancyhf{}',
        r'\begin{document}'
    ]

def latex_name_contact(data):
    name = data.get('name', {})
    contact = data.get('contact', {})
    return [
        rf"\namesection{{{name.get('first','John')}}}{{{name.get('last','Doe')}}}{{",
        rf"\href{{mailto:{contact.get('email','johndoe@email.com')}}}{{{contact.get('email','johndoe@email.com')}}} | ",
        rf"\href{{{contact.get('portfolio','https://johndoe.com')}}}{{Portfolio}} | ",
        rf"\href{{{contact.get('github','https://github.com/johndoe')}}}{{GitHub}} | ",
        rf"\href{{{contact.get('linkedin','https://linkedin.com/in/johndoe')}}}{{LinkedIn}}",
        r'}'
    ]

def latex_education_skills(data):
    tex = [r'\begin{minipage}[t]{0.33\textwidth}', r'\section{Education}']
    for edu in data.get('education', []):
        tex.append(rf"\subsection{{{edu.get('institution','')}}}")
        tex.append(rf"\descript{{{edu.get('degree','')}}}")
        tex.append(rf"\location{{{edu.get('location','')}}}")
        tex.append(rf"{edu.get('description','')} \\" )
    tex.append(r'\sectionsep')
    tex.append(r'\section{Skills}')
    for skill in data.get('skills', []):
            tex.append(rf"{skill} \\")
    tex.append(r'\end{minipage}')
    return tex

def latex_experience(data):
    tex = [r'\begin{minipage}[t]{0.66\textwidth}', r'\section{Experience}']
    for exp in data.get('experience', []):
        tex.append(rf"\runsubsection{{{exp.get('company','')}}}")
        tex.append(rf"\descript{{{exp.get('position','')}}}")
        tex.append(rf"\location{{{exp.get('location','')}}}")
        tex.append(rf"{exp.get('description','')} \\" )
        tex.append(r'\sectionsep')
    return tex

def latex_projects(data):
    tex = [r'\section{Projects}']
    for proj in data.get('projects', []):
        tex.append(rf"\runsubsection{{{proj.get('name','')}}}")
        if proj.get('url'):
            tex.append(rf"\href{{{proj.get('url')}}}{{{proj.get('url')}}} \\" )
        tex.append(rf"{proj.get('description','')} \\" )
        tex.append(r'\sectionsep')
    return tex

def latex_awards(data):
    tex = [r'\section{Awards}']
    for award in data.get('awards', []):
        tex.append(rf"\descript{{{award.get('title','')}}}")
        tex.append(rf"{award.get('year','')} - {award.get('description','')} \\\\")
        tex.append(r'\sectionsep')
    tex.append(r'\end{minipage}')
    tex.append(r'\end{document}')
    return tex

def generate_resume(yaml_path='resume.yaml', tex_path='resume.tex', cls_file=None):
    yaml_path = Path(yaml_path)
    tex_path = Path(tex_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f'{yaml_path} not found. Please fill in your details.')
    with yaml_path.open() as f:
        data = yaml.safe_load(f)
    if cls_file:
        data['cls'] = cls_file

    tex = []
    tex += latex_header(data)
    tex += latex_name_contact(data)
    tex += latex_education_skills(data)
    tex += latex_experience(data)
    tex += latex_projects(data)
    tex += latex_awards(data)
    # Ensure resume.tex is overwritten or deleted before writing
    if tex_path.exists():
        tex_path.unlink()  # Delete existing file
    tex_path.write_text('\n'.join(tex))
    return str(tex_path)
