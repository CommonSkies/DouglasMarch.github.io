#!/bin/csh
latex JP1-2.tex
latex JP1-2.tex
dvips -o JP1-2.ps JP1-2.dvi
ps2pdf JP1-2.ps
