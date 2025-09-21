% Minimalist CV Class
\ProvidesClass{minimalist}[2025/09/22 Minimalist CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=2cm, vmargin=2cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Minimalist Colors
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{primary}{HTML}{222222}
\definecolor{headings}{HTML}{444444}
\definecolor{subheadings}{HTML}{888888}

% Fonts
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\renewcommand{\rmdefault}{lmr} % Latin Modern Roman

% Section formatting
\usepackage{titlesec}
\titleformat{\section}{\color{headings}\scshape\fontsize{16pt}{24pt}\selectfont\raggedright\uppercase}{}{0em}{}
\titleformat{\subsection}{\color{subheadings}\fontsize{12pt}{14pt}\selectfont\bfseries}{}{0em}{}

% Name command
\newcommand{\namesection}[3]{
\centering{\fontsize{36pt}{54pt}\selectfont\textbf{#1 #2}} \\[5pt]
\centering{\color{headings}\fontsize{10pt}{14pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{headings}\rule{\paperwidth}{0.2pt}}
\vspace{-10pt}
}

% Section separator
\newcommand{\sectionsep}{\vspace{6pt}}

% Bullet Lists
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}
