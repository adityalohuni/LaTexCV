% Art Deco CV Class
\ProvidesClass{artdeco}[2025/09/22 Art Deco CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=1.2cm, vmargin=1cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Art Deco Colors
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{primary}{HTML}{CBA135}
\definecolor{headings}{HTML}{2E4053}
\definecolor{subheadings}{HTML}{BFC9CA}
\definecolor{accent}{HTML}{F7DC6F}

% Fonts
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\renewcommand{\rmdefault}{pnc} % Palatino for Art Deco

% Section formatting
\usepackage{titlesec}
\titleformat{\section}{\color{headings}\scshape\fontsize{17pt}{26pt}\selectfont\raggedright\uppercase}{}{0em}{}
\titleformat{\subsection}{\color{subheadings}\fontsize{13pt}{15pt}\selectfont\bfseries\uppercase}{}{0em}{}

% Name command
\newcommand{\namesection}[3]{
\centering{\fontsize{40pt}{60pt}\selectfont\textbf{#1 #2}} \\[5pt]
\centering{\color{headings}\fontsize{11pt}{15pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{primary}\rule{\paperwidth}{1pt}}
\vspace{-15pt}
}

% Section separator
\newcommand{\sectionsep}{\vspace{9pt}}

% Bullet Lists
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep2pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}
