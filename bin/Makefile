# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001-2008 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# $Id: Makefile 969 2007-03-29 17:41:54Z johnholland $

ROFF=/usr/bin/groff
PROG=/usr/local/bin/man2html
MANDIR=.
OUTPUTDIR=../../pyx12-web/doc
MANS=

all: pyx12.conf.xml.5.html x12html.1.html x12norm.1.html x12valid.1.html x12xml.1.html xmlx12.1.html

pyx12.conf.xml.5.html: pyx12.conf.xml.5
	${ROFF} -man -Tascii pyx12.conf.xml.5 | ${PROG} > ${OUTPUTDIR}/pyx12.conf.xml.5.html

x12html.1.html: x12html.1
	${ROFF} -man -Tascii x12html.1 | ${PROG} > ${OUTPUTDIR}/x12html.1.html

x12norm.1.html: x12norm.1
	${ROFF} -man -Tascii x12norm.1 | ${PROG} > ${OUTPUTDIR}/x12norm.1.html

x12valid.1.html: x12valid.1
	${ROFF} -man -Tascii x12valid.1 | ${PROG} > ${OUTPUTDIR}/x12valid.1.html

x12xml.1.html: x12xml.1
	${ROFF} -man -Tascii x12xml.1 | ${PROG} > ${OUTPUTDIR}/x12xml.1.html

xmlx12.1.html: xmlx12.1
	${ROFF} -man -Tascii xmlx12.1 | ${PROG} > ${OUTPUTDIR}/xmlx12.1.html
