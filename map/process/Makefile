# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# #Id$

TRANS=/usr/local/bin/xsltproc
LINT=/usr/local/bin/xmllint
XSL=loop_id.xsl
FLAGS=

all: 
	${TRANS} ${FLAGS} ${XSL} 270.4010.X092.A1.xml | ${LINT} --format -o 270.4010.X092.A1.xml -
	${TRANS} ${FLAGS} ${XSL} 270.4010.X092.xml | ${LINT} --format -o 270.4010.X092.xml -
	${TRANS} ${FLAGS} ${XSL} 271.4010.X092.A1.xml | ${LINT} --format -o 271.4010.X092.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 271.4010.X092.xml | ${LINT} --format -o 271.4010.X092.xml - 
	${TRANS} ${FLAGS} ${XSL} 276.4010.X093.A1.xml | ${LINT} --format -o 276.4010.X093.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 276.4010.X093.xml | ${LINT} --format -o 276.4010.X093.xml - 
	${TRANS} ${FLAGS} ${XSL} 277.4010.X093.A1.xml | ${LINT} --format -o 277.4010.X093.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 277.4010.X093.xml | ${LINT} --format -o 277.4010.X093.xml - 
	${TRANS} ${FLAGS} ${XSL} 278.4010.X094.27.A1.xml | ${LINT} --format -o 278.4010.X094.27.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 278.4010.X094.27.xml | ${LINT} --format -o 278.4010.X094.27.xml - 
	${TRANS} ${FLAGS} ${XSL} 278.4010.X094.A1.xml | ${LINT} --format -o 278.4010.X094.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 278.4010.X094.xml | ${LINT} --format -o 278.4010.X094.xml - 
	${TRANS} ${FLAGS} ${XSL} 820.4010.X061.A1.xml | ${LINT} --format -o 820.4010.X061.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 820.4010.X061.xml | ${LINT} --format -o 820.4010.X061.xml - 
	${TRANS} ${FLAGS} ${XSL} 834.4010.X095.A1.xml | ${LINT} --format -o 834.4010.X095.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 835.4010.X091.A1.xml | ${LINT} --format -o 835.4010.X091.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 835.4010.X091.xml | ${LINT} --format -o 835.4010.X091.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X096.A1.xml | ${LINT} --format -o 837.4010.X096.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X096.xml | ${LINT} --format -o 837.4010.X096.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X097.A1.xml | ${LINT} --format -o 837.4010.X097.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X097.xml | ${LINT} --format -o 837.4010.X097.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X098.A1.xml | ${LINT} --format -o 837.4010.X098.A1.xml - 
	${TRANS} ${FLAGS} ${XSL} 837.4010.X098.xml | ${LINT} --format -o 837.4010.X098.xml - 
	${TRANS} ${FLAGS} ${XSL} 841.4010.XXXC.xml | ${LINT} --format -o 841.4010.XXXC.xml - 
	${TRANS} ${FLAGS} ${XSL} 997.4010.xml | ${LINT} --format -o 997.4010.xml - 
	${TRANS} ${FLAGS} ${XSL} x12.control.00401.xml | ${LINT} --format -o x12.control.00401.xml - 
