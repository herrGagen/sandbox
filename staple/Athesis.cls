\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{Athesis}[1999/08/01 SUNY Stony Brook thesis class]


\newif\if@ttop
\newif\if@sig

\DeclareOption{master}{%
     \newcommand{\@work}{Thesis}%
     \newcommand{\@degree}{Master of Science}}
\DeclareOption{phd}{%
     \newcommand{\@work}{Dissertation}%
     \newcommand{\@degree}{Doctor of Philosophy}}
\DeclareOption{ttop}{\@ttoptrue}
\DeclareOption{tbottom}{\@ttopfalse}
\DeclareOption{tsig}{\@sigtrue}
\DeclareOption{tnosig}{\@sigfalse}
\DeclareOption*{\PackageWarning{usbthesis}{This package does not 
recognize option: \CurrentOption}}
%\ExecuteOptions{phd,bottom}
\ProcessOptions\relax

\LoadClass[letterpaper,12pt,oneside]{report}

\RequirePackage{setspace}
\doublespacing
\RequirePackage{vmargin}
\setpapersize{USletter}

%\setmargins{1.5in}{1.25in}{5.5in}{8.125in}{0.125in}{0.75in}{0.125in}{0.325in}
%\setmargins{1.5in}{1.25in}{5.5in}{8.125in}{0.125in}{0.2in}{0.125in}{0.5in}

\if@ttop
     \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.75in}{0.125in}{0.325in}
\else
     \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
\fi

%\renewcommand{\LARGE}{\Large}
%\renewcommand{\huge}{\Large}
%\renewcommand{\Huge}{\LARGE}
%\renewcommand{\Huge}{\Large}

\renewcommand{\month}{August}
\renewcommand{\year}{2014}

\newcommand{\ps@prelim}{%
     \pagenumbering{roman}%
     \renewcommand{\@oddhead}{}%
     \renewcommand{\@evenhead}{}%
     \renewcommand{\@evenfoot}{\hfil\textrm{\thepage}\hfil}%
     \renewcommand{\@oddfoot}{\@evenfoot}}
\newcommand{\ps@thesis}{%
     \pagenumbering{arabic}%
     \if@ttop
     \renewcommand{\@oddfoot}{}%
     \renewcommand{\@evenfoot}{}%
     \renewcommand{\@evenhead}{\hskip-0.25in \textrm{\thepage}\hfil}%
     \renewcommand{\@oddhead}{\hfil \textrm{\thepage} \hskip-0.25in}%
     \renewcommand{\ps@plain}{%
         \renewcommand{\@oddfoot}{}%
         \renewcommand{\@evenfoot}{}%
         \renewcommand{\@evenhead}{\hskip-0.25in \textrm{\thepage}\hfil}%
         \renewcommand{\@oddhead}{\hfil\textrm{\thepage} \hskip-0.25in}}
     \fi
}

\newcommand{\program}[1]{%
     \newcommand{\@program}{#1}}
\newcommand{\director}[2]{%
     \newcommand{\@directorname}{#1}%
     \newcommand{\@directorposition}{#2}}
\newcommand{\chairman}[2]{%
     \newcommand{\@chairmanname}{#1}%
     \newcommand{\@chairmanposition}{#2}}
\newcommand{\fstmember}[2]{%
     \newcommand{\@fstmembername}{#1}%
     \newcommand{\@fstmemberposition}{#2}}
\newcommand{\sndmember}[2]{%
     \newcommand{\@sndmembername}{#1}%
     \newcommand{\@sndmemberposition}{#2}}
\newcommand{\trdmember}[2]{%
     \newcommand{\@trdmembername}{#1}%
     \newcommand{\@trdmemberposition}{#2}}
\newcommand{\outmember}[3]{%
     \newcommand{\@outmembername}{#1}%
     \newcommand{\@outmemberposition}{#2}%
     \newcommand{\@outmemberschool}{#3}}
\newcommand{\dean}[1]{%
     \newcommand{\@dean}{#1}}

\renewcommand{\maketitle}{\begin{titlepage}%
     \if@ttop
     \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \renewcommand{\footnotesize}{\small} %\let\footnoterule\relax
     \setcounter{page}{0}%
     \begin{center}%
     \setlength{\baselineskip}{29pt}%
%     \vspace*{0.2in}%
     {\LARGE\textbf{\@title}}\\%

     \vfill 
     \setlength{\baselineskip}{14.5pt}
%     \large
%     [0.2in] 
     A \@work\ Presented\\%
%     [0.2in] \vfill A \@work, Presented\\%
     [0.2in] by\\%
     [0.25in] \textbf{\large \@author} \\%
     [0.25in] to\\%
     [0.2in] The Graduate School\\%
     [0.2in] in Partial Fulfillment of the Requirements\\
%     [0.2in] Requirements\\%
     [0.2in] for the Degree of\\%
     [0.5in] \textbf{\large \@degree}\\%
     [0.2in] in\\%
     [0.2in] \textbf{\large \@program}\\%
     [0.5in] Stony Brook University\\%
     [0.2in] \month\ \year%
     \end{center}%
     \par\null%
     \setcounter{footnote}{0}%
     \let\thanks\relax%
     \let\maketitle\relax%
\end{titlepage}}

\newcommand{\makeapproval}{%
     \if@ttop
     \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \pagestyle{prelim}
     \setcounter{page}{2}%
     \begin{center}%
     \setlength{\baselineskip}{14.5pt}%
     \textbf{Stony Brook University}\\%
     [0.1in]{The Graduate School} \\%
     [0.35in] \textbf{\large \@author}%
     \end{center}%
     \vspace{0.25in}%
     {\setlength{\baselineskip}{14.5pt}%
     We, the \MakeLowercase{\@work}\ committee for the above candidate for the
     \@degree\ degree, hereby recommend acceptance of this \MakeLowercase{\@work}.\par}
     \begin{center}%
     \setlength{\baselineskip}{14.5pt}%

     \rule[-0.55in]{3in}{\if@sig 0.01in \else 0.00in \fi}\\
     [0.03in]\@directorname{} -- \@work{} Advisor\\
     \@directorposition\\%
 
     \rule[-0.55in]{3in}{\if@sig 0.01in \else 0.00in \fi}\\
     [0.03in]\@chairmanname{} -- Chairperson of Defense\\
     \@chairmanposition\\%
 
     \rule[-0.55in]{3in}{\if@sig 0.01in \else 0.00in \fi}\\
     [0.03in]\@fstmembername\\
     \@fstmemberposition\\%

     \rule[-0.55in]{3in}{\if@sig 0.01in \else 0.00in \fi}\\
     [0.03in]\@sndmembername\\
     \@sndmemberposition\\%

     \end{center}%

     \vspace{0.2in}%
     This \MakeLowercase{\@work}\ is accepted by the Graduate School.
     \begin{flushright}%
     \parbox{\if@sig 3in \else 2.5in \fi}%
     {\centering%\raggedright%
     \baselineskip 14.5pt%
     \rule[-0.55in]{3in}{\if@sig 0.01in \else 0.00in \fi}\\[0.03in]
     \if@sig \else \@dean\\ \fi
     \@dean \\ Dean of the Graduate School\\}%
     \end{flushright}\clearpage}

\renewenvironment{abstract}{%
    \if@ttop
    \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
    \fi
    \begin{center}%
    \setlength{\baselineskip}{14.5pt}%
    \vspace*{0.1in}%
    {\Large Abstract of the \@work}\\%
    [0.2in]{\textbf{\Large{\@title}}}\\%
%    [0.2in]{\Huge{\@title}}\\%
%    {\bf \sc \Huge {\@title\\}}%
    \vspace{0.2in} by \\%
%    [0.2in]by\\%
    [0.2in]\textbf{\large \@author}\\%
    [0.3in]\textbf{\large \@degree}\\%
    [0.2in]in\\%
    [0.2in]\textbf{\large \@program}\\%
    [0.2in]{\large Stony Brook University} \\
    [0.2in]{\large \year}\\%
    [0.2in]\if@sig {\large \@directorname} \fi %for extra abstract copy
    \end{center}%
    \par%
    \vspace{0.4in}%
    \begin{quote}}%
    {\end{quote}%
    %\par\vfil\null
    \clearpage}
     

\newenvironment{dedication}{%
     \if@ttop
    \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \thispagestyle{empty}%
     \pagestyle{empty}
     \vspace*{\fill}%
     \begin{center}}%
     {\end{center}\vspace*{\fill}\clearpage}

\newenvironment{acknowledgements}{%
     \if@ttop
    \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \clearpage%
     \phantomsection
     \addcontentsline{toc}{chapter}{\protect\numberline{}{Acknowledgements}}
     \chapter*{Acknowledgements}%
     \thispagestyle{empty}%
     \pagestyle{empty}}%
     {\clearpage}

\renewenvironment{thebibliography}[1]
      {\chapter*{\bibname
         \@mkboth{\MakeUppercase\bibname}{\MakeUppercase\bibname}}%
       \list{\@biblabel{\@arabic\c@enumiv}}%
            {\settowidth\labelwidth{\@biblabel{#1}}%
             \leftmargin\labelwidth
             \advance\leftmargin\labelsep
             \@openbib@code
             \usecounter{enumiv}%
             \let\p@enumiv\@empty
             \renewcommand\theenumiv{\@arabic\c@enumiv}}%
       \sloppy
       \clubpenalty4000
       \@clubpenalty \clubpenalty
       \widowpenalty4000%
       \sfcode`\.\@m}
      {\def\@noitemerr
        {\@latex@warning{Empty `thebibliography' environment}}%
       \endlist
       \addcontentsline{toc}{chapter}{\protect\numberline{}{\bibname
         \@mkboth{\MakeUppercase\bibname}{\MakeUppercase\bibname}}}}

\renewcommand\listoffigures{%
     \if@ttop
    \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \if@twocolumn
       \@restonecoltrue\onecolumn
     \else
       \@restonecolfalse
     \fi
     \clearpage
     \phantomsection
     \addcontentsline{toc}{chapter}{\protect\numberline{}{\listfigurename
       \@mkboth{\MakeUppercase\listfigurename}{\MakeUppercase\listfigurename}}}%
     \chapter*{\listfigurename
       \@mkboth{\MakeUppercase\listfigurename}%
               {\MakeUppercase\listfigurename}}%
     \@starttoc{lof}%
     \if@restonecol\twocolumn\fi
     }

\renewcommand\listoftables{%
     \if@ttop
    \setmarginsrb{1.5in}{1in}{1.5in}{1in}{0.125in}{0.2in}{0.125in}{0.5in}
     \fi
     \if@twocolumn
       \@restonecoltrue\onecolumn
     \else
       \@restonecolfalse
     \fi
     \clearpage
     \phantomsection
     \addcontentsline{toc}{chapter}{\protect\numberline{}{\listtablename
       \@mkboth{\MakeUppercase\listtablename}{\MakeUppercase\listtablename}}}%
     \chapter*{\listtablename
       \@mkboth{%
           \MakeUppercase\listtablename}{\MakeUppercase\listtablename}}%
     \@starttoc{lot}%
     \if@restonecol\twocolumn\fi
     }
