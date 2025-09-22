% Art Deco CV Class
\ProvidesClass{artdeco}[2025/09/22 Art Deco CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Geometry and Hyperref
\usepackage[hmargin=1.5cm, vmargin=1cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Art Deco Colors (updated palette)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{decoGold}{HTML}{CBA135}
\definecolor{decoRed}{HTML}{B03A2E}
\definecolor{decoBlue}{HTML}{2874A6}
\definecolor{decoGreen}{HTML}{229954}
\definecolor{decoGray}{HTML}{2E4053}
\definecolor{decoAccent}{HTML}{F7DC6F}
\definecolor{decoSilver}{HTML}{BFC9CA}

% Fonts
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\renewcommand{\rmdefault}{pnc} % Palatino for Art Deco

% Section formatting (match Bauhaus/Deedy)
\usepackage{titlesec}
\titleformat{\section}{\color{decoRed}
\scshape\fontsize{16pt}{24pt}\selectfont \raggedright\uppercase}{}{0em}{}
\titleformat{\subsection}{\color{decoBlue}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase}{}{0em}{}
% Section spacing (from deedy.cls)
\titlespacing{\section}{0pt}{0pt}{0pt}
\titlespacing{\subsection}{0pt}{0pt}{0pt}

% Name command (match Bauhaus/Deedy)
\newcommand{\namesection}[3]{
\centering{\fontsize{40pt}{60pt}\selectfont\textbf{#1 #2}} \\[5pt]
\centering{\color{decoGray}\fontsize{11pt}{14pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{decoGold}\rule{\paperwidth}{0.4pt}}
\vspace{-15pt}
}

% Date command (from deedy.cls, Art Deco colors)
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{isodate}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\newcommand{\lastupdated}{\begin{textblock}{60}(155,5)
\color{decoSilver}\fontsize{8pt}{10pt}\selectfont 
Last Updated on \today
\end{textblock}}

% Subsection heading (from deedy.cls, Art Deco colors)
\newcommand{\runsubsection}[1]{
\color{decoBlue}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase {#1} \normalfont}

% Descriptors (from deedy.cls, Art Deco colors)
\newcommand{\descript}[1]{
\color{decoAccent}\raggedright\scshape\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location (from deedy.cls, Art Deco colors)
\newcommand{\location}[1]{
\color{decoGray}\raggedright\fontsize{10pt}{12pt}\selectfont {#1\\} \normalfont}
}

% Section separator (match Bauhaus/Deedy)
\newcommand{\sectionsep}{\vspace{8pt}}

% Bullet Lists (match Bauhaus/Deedy)
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}
