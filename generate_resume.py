import yaml
from pathlib import Path

def main():
    yaml_path = Path('resume.yaml')
    tex_path = Path('resume.tex')
    if not yaml_path.exists():
        print('resume.yaml not found. Please fill in your details.')
        return
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    # Start LaTeX content
    tex = []
    tex.append(r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    tex.append(r'% Deedy - One Page Two Column Resume')
    tex.append(r'% Auto-generated from resume.yaml')
    tex.append(r'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    tex.append(r'\documentclass[]{deedy-resume}')
    tex.append(r'\usepackage{fancyhdr}')
    tex.append(r'\usepackage{hyperref}')
    tex.append(r'\usepackage{fontawesome}')
    tex.append(r'\usepackage[usenames,dvipsnames]{xcolor}')
    tex.append(r'\pagestyle{fancy}')
    tex.append(r'\fancyhf{}')
    tex.append(r'\begin{document}')
    # Name and contact
    name = data.get('name', {})
    contact = data.get('contact', {})
    tex.append(rf"\namesection{{{name.get('first','John')}}}{{{name.get('last','Doe')}}}{{")
    tex.append(rf"\href{{mailto:{contact.get('email','johndoe@email.com')}}}{{{contact.get('email','johndoe@email.com')}}} | ")
    tex.append(rf"\href{{{contact.get('portfolio','https://johndoe.com')}}}{{Portfolio}} | ")
    tex.append(rf"\href{{{contact.get('github','https://github.com/johndoe')}}}{{GitHub}} | ")
    tex.append(rf"\href{{{contact.get('linkedin','https://linkedin.com/in/johndoe')}}}{{LinkedIn}}")
    tex.append(r'}')
    # Column one: Education & Skills
    tex.append(r'\begin{minipage}[t]{0.33\textwidth}')
    tex.append(r'\section{Education}')
    for edu in data.get('education', []):
        tex.append(rf"\subsection{{{edu.get('institution','')}}}")
        tex.append(rf"\descript{{{edu.get('degree','')}}}")
        tex.append(rf"\location{{{edu.get('location','')}}}")
    tex.append(rf"{edu.get('description','')} \\")
    tex.append(r'\sectionsep')
    tex.append(r'\section{Skills}')
    for skill in data.get('skills', []):
        tex.append(rf"{skill} \\")
    tex.append(r'\end{minipage}')
    # Column two: Experience, Projects, Awards
    tex.append(r'\begin{minipage}[t]{0.66\textwidth}')

    # Experience
    tex.append(r'\section{Experience}')
    for exp in data.get('experience', []):
        tex.append(rf"\runsubsection{{{exp.get('company','')}}}")
        tex.append(rf"\descript{{{exp.get('position','')}}}")
        tex.append(rf"\location{{{exp.get('location','')}}}")
        tex.append(rf"{exp.get('description','')} \\")
        tex.append(r'\sectionsep')

    # Projects
    tex.append(r'\section{Projects}')
    for proj in data.get('projects', []):
        tex.append(rf"\runsubsection{{{proj.get('name','')}}}")
        if proj.get('url'):
            tex.append(rf"\href{{{proj.get('url')}}}{{{proj.get('url')}}} \\")
        tex.append(rf"{proj.get('description','')} \\")
        tex.append(r'\sectionsep')

    # Awards
    tex.append(r'\section{Awards}')
    for award in data.get('awards', []):
        tex.append(rf"\descript{{{award.get('title','')}}}")
        tex.append(rf"{award.get('year','')} - {award.get('description','')} \\")
        tex.append(r'\sectionsep')

    tex.append(r'\end{minipage}')
    tex.append(r'\end{document}')
    with open(tex_path, 'w') as f:
        f.write('\n'.join(tex))
    print('resume.tex generated from resume.yaml.')

if __name__ == '__main__':
    main()
