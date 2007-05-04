# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# $Id: Makefile 969 2007-03-29 17:41:54Z johnholland $

PROG=/usr/local/bin/man2html
MANDIR=.
OUTPUTDIR=../../pyx12-web/doc
MANS=

all: pyx12.conf.xml.5.html x12html.1.html x12norm.1.html x12valid.1.html x12xml.1.html

pyx12.conf.xml.5.html: pyx12.conf.xml.5
	${PROG} < pyx12.conf.xml.5 > ${OUTPUTDIR}/pyx12.conf.xml.5.html

x12html.1.html: x12html.1
	${PROG} < x12html.1 > ${OUTPUTDIR}/x12html.1.html

x12norm.1.html: x12norm.1
	${PROG} < x12norm.1 > ${OUTPUTDIR}/x12norm.1.html

x12valid.1.html: x12valid.1
	${PROG} < x12valid.1 > ${OUTPUTDIR}/x12valid.1.html

x12xml.1.html: x12xml.1
	${PROG} < x12xml.1 > ${OUTPUTDIR}/x12xml.1.html
