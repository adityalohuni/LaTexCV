% Bauhaus CV Class
\ProvidesClass{bauhaus}[2025/09/22 Bauhaus CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Geometry
\usepackage[hmargin=1.5cm, vmargin=1cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Bauhaus Colors
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{bhRed}{HTML}{E53935}
\definecolor{bhBlue}{HTML}{1E88E5}
\definecolor{bhYellow}{HTML}{FDD835}
\definecolor{bhGray}{HTML}{212121}
\definecolor{bhAccent}{HTML}{43A047}

% Fonts: Use Fira Sans if available, else Helvetica
\IfFileExists{FiraSans-Regular.otf}{
  \usepackage[sfdefault]{FiraSans}
}{
  \renewcommand{\rmdefault}{phv}
  \renewcommand{\sfdefault}{phv}
}

% Date command
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{isodate}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\newcommand{\lastupdated}{\begin{textblock}{60}(155,5)
\color{bhGray}\fontsize{8pt}{10pt}\selectfont 
Last Updated on \today
\end{textblock}}

% Name section
\newcommand{\namesection}[3]{
\centering{
\fontsize{40pt}{60pt}
\selectfont\textbf{#1 #2}
} \\[5pt]
\centering{
\color{bhAccent}
\fontsize{11pt}{14pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{bhYellow}\rule{\paperwidth}{0.4pt}}
\vspace{-15pt}
}

% Section separators
\usepackage{titlesec}
\titlespacing{\section}{0pt}{0pt}{0pt} 
\titlespacing{\subsection}{0pt}{0pt}{0pt}
\newcommand{\sectionsep}{\vspace{8pt}}

% Headings
\titleformat{\section}{\color{bhRed}
\scshape\fontsize{16pt}{24pt}\selectfont \raggedright\uppercase}{}{0em}{}

% Subheadings
\titleformat{\subsection}{
\color{bhBlue}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase}{}{0em}{}

\newcommand{\runsubsection}[1]{
\color{bhBlue}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase {#1} \normalfont}

% Descriptors
\newcommand{\descript}[1]{
\color{bhAccent}\raggedright\scshape\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location
\newcommand{\location}[1]{
\color{bhGray}\raggedright\fontsize{10pt}{12pt}\selectfont {#1\\} \normalfont}

% Bullet Lists with fewer gaps
\newenvironment{tightemize}{
\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}
{\end{itemize}\vspace{-\topsep}}
