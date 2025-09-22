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
\usepackage[hmargin=1.5cm, vmargin=1cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Minimalist Colors (refined)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{minPrimary}{HTML}{222222}
\definecolor{minHeading}{HTML}{444444}
\definecolor{minSubheading}{HTML}{888888}
\definecolor{minAccent}{HTML}{007ACC}

% Fonts
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\renewcommand{\rmdefault}{lmr} % Latin Modern Roman

% Section formatting (match Bauhaus/Deedy)
\usepackage{titlesec}
\titleformat{\section}{\color{minHeading}\scshape\fontsize{16pt}{24pt}\selectfont\raggedright\uppercase}{}{0em}{}
\titleformat{\subsection}{\color{minAccent}\fontsize{12pt}{12pt}\selectfont\bfseries}{}{0em}{}
% Section spacing (from deedy.cls)
\titlespacing{\section}{0pt}{0pt}{0pt}
\titlespacing{\subsection}{0pt}{0pt}{0pt}

% Name command (match Bauhaus/Deedy)
\newcommand{\namesection}[3]{
\centering{\fontsize{40pt}{60pt}\selectfont\textbf{#1 #2}} \\[5pt]
\centering{\color{minHeading}\fontsize{11pt}{14pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{minPrimary}\rule{\paperwidth}{0.4pt}}
\vspace{-15pt}
}

% Date command (from deedy.cls, minimalist colors)
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{isodate}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\newcommand{\lastupdated}{\begin{textblock}{60}(155,5)
\color{minSubheading}\fontsize{8pt}{10pt}\selectfont 
Last Updated on \today
\end{textblock}}

% Subsection heading (from deedy.cls, minimalist colors)
\newcommand{\runsubsection}[1]{
\color{minAccent}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase {#1} \normalfont}

% Descriptors (from deedy.cls, minimalist colors)
\newcommand{\descript}[1]{
\color{minAccent}\raggedright\scshape\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location (from deedy.cls, minimalist colors)
\newcommand{\location}[1]{
\color{minSubheading}\raggedright\fontsize{10pt}{12pt}\selectfont {#1\\} \normalfont}

% Section separator (match Bauhaus/Deedy)
\newcommand{\sectionsep}{\vspace{8pt}}

% Bullet Lists (match Bauhaus/Deedy)
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}
