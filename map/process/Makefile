# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# #Id$

XSLT=/usr/local/bin/xsltproc
LINT=/usr/local/bin/xmllint
XSL=trn_id.xsl
XFLAGS=
LFLAGS=--format

all: 
	${XSLT} ${XFLAGS} ${XSL} 270.4010.X092.A1.xml | ${LINT} ${LFLAGS} -o 270.4010.X092.A1.xml -
	${XSLT} ${XFLAGS} ${XSL} 271.4010.X092.A1.xml | ${LINT} ${LFLAGS} -o 271.4010.X092.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 276.4010.X093.A1.xml | ${LINT} ${LFLAGS} -o 276.4010.X093.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 277.4010.X093.A1.xml | ${LINT} ${LFLAGS} -o 277.4010.X093.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 277.4020.X104.xml | ${LINT} ${LFLAGS} -o 277.4020.X104.xml - 
	${XSLT} ${XFLAGS} ${XSL} 277U.4010.X070.xml | ${LINT} ${LFLAGS} -o 277U.4010.X070.xml - 
	${XSLT} ${XFLAGS} ${XSL} 278.4010.X094.27.A1.xml | ${LINT} ${LFLAGS} -o 278.4010.X094.27.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 278.4010.X094.A1.xml | ${LINT} ${LFLAGS} -o 278.4010.X094.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 820.4010.X061.A1.xml | ${LINT} ${LFLAGS} -o 820.4010.X061.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 834.4010.X095.A1.xml | ${LINT} ${LFLAGS} -o 834.4010.X095.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 835.4010.X091.A1.xml | ${LINT} ${LFLAGS} -o 835.4010.X091.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 837.4010.X096.A1.xml | ${LINT} ${LFLAGS} -o 837.4010.X096.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 837.4010.X097.A1.xml | ${LINT} ${LFLAGS} -o 837.4010.X097.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 837.4010.X098.A1.xml | ${LINT} ${LFLAGS} -o 837.4010.X098.A1.xml - 
	${XSLT} ${XFLAGS} ${XSL} 841.4010.XXXC.xml | ${LINT} ${LFLAGS} -o 841.4010.XXXC.xml - 
	${XSLT} ${XFLAGS} ${XSL} 997.4010.xml | ${LINT} ${LFLAGS} -o 997.4010.xml - 
	${XSLT} ${XFLAGS} ${XSL} x12.control.00401.xml | ${LINT} ${LFLAGS} -o x12.control.00401.xml - 
