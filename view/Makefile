# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# #Id$

TRANS=/usr/local/bin/xsltproc
MAPDIR=../map
MAPS=270 271 276 277 278 820 835 837D 837I 837P

all: ${MAPS} codes

270: 270.sum.html 270.seg.html 270.loop.html

271: 271.sum.html 271.seg.html 271.loop.html

276: 276.sum.html 276.seg.html 276.loop.html

277: 277.sum.html 277.seg.html 277.loop.html

278: 278.sum.27.html 278.seg.27.html 278.sum.html 278.seg.html 278.loop.html 278.loop.27.html

820: 820.sum.html 820.seg.html 820.loop.html

835: 835.sum.html 835.seg.html 835.loop.html

#837: 837I 837D 837P

837I: 837.X096.sum.html 837.X096.seg.html 837.X096.loop.html

837D: 837.X097.sum.html 837.X097.seg.html 837.X097.loop.html

837P: 837.X098.sum.html 837.X098.seg.html 837.X098.loop.html

codes: codes.html 

codes.html: ${MAPDIR}/codes.xml
	${TRANS} -o codes.html codes.xsl ${MAPDIR}/codes.xml

codes.html: codes.xsl

270.sum.html: ${MAPDIR}/map.270.4010.X092.xml
	${TRANS} -o 270.sum.html map_sum.xsl ${MAPDIR}/map.270.4010.X092.xml

271.sum.html: ${MAPDIR}/map.271.4010.X092.xml
	${TRANS} -o 271.sum.html map_sum.xsl ${MAPDIR}/map.271.4010.X092.xml

276.sum.html: ${MAPDIR}/map.276.4010.X093.xml
	${TRANS} -o 276.sum.html map_sum.xsl ${MAPDIR}/map.276.4010.X093.xml

277.sum.html: ${MAPDIR}/map.277.4010.X093.xml
	${TRANS} -o 277.sum.html map_sum.xsl ${MAPDIR}/map.277.4010.X093.xml

278.sum.27.html: ${MAPDIR}/map.278.4010.X094.27.xml
	${TRANS} -o 278.sum.27.html map_sum.xsl ${MAPDIR}/map.278.4010.X094.27.xml

278.sum.html: ${MAPDIR}/map.278.4010.X094.xml
	${TRANS} -o 278.sum.html map_sum.xsl ${MAPDIR}/map.278.4010.X094.xml

820.sum.html: ${MAPDIR}/map.820.4010.X061.xml
	${TRANS} -o 820.sum.html map_sum.xsl ${MAPDIR}/map.820.4010.X061.xml

835.sum.html: ${MAPDIR}/map.835.4010.X091.xml
	${TRANS} -o 835.sum.html map_sum.xsl ${MAPDIR}/map.835.4010.X091.xml

837.X096.sum.html: ${MAPDIR}/map.837.4010.X096.xml
	${TRANS} -o 837.X096.sum.html map_sum.xsl ${MAPDIR}/map.837.4010.X096.xml

837.X097.sum.html: ${MAPDIR}/map.837.4010.X097.xml
	${TRANS} -o 837.X097.sum.html map_sum.xsl ${MAPDIR}/map.837.4010.X097.xml

837.X098.sum.html: ${MAPDIR}/map.837.4010.X098.xml
	${TRANS} -o 837.X098.sum.html map_sum.xsl ${MAPDIR}/map.837.4010.X098.xml

270.seg.html: ${MAPDIR}/map.270.4010.X092.xml
	${TRANS} -o 270.seg.html map_seg.xsl ${MAPDIR}/map.270.4010.X092.xml

271.seg.html: ${MAPDIR}/map.271.4010.X092.xml
	${TRANS} -o 271.seg.html map_seg.xsl ${MAPDIR}/map.271.4010.X092.xml

276.seg.html: ${MAPDIR}/map.276.4010.X093.xml
	${TRANS} -o 276.seg.html map_seg.xsl ${MAPDIR}/map.276.4010.X093.xml

277.seg.html: ${MAPDIR}/map.277.4010.X093.xml
	${TRANS} -o 277.seg.html map_seg.xsl ${MAPDIR}/map.277.4010.X093.xml

278.seg.27.html: ${MAPDIR}/map.278.4010.X094.27.xml
	${TRANS} -o 278.seg.27.html map_seg.xsl ${MAPDIR}/map.278.4010.X094.27.xml

278.seg.html: ${MAPDIR}/map.278.4010.X094.xml
	${TRANS} -o 278.seg.html map_seg.xsl ${MAPDIR}/map.278.4010.X094.xml

820.seg.html: ${MAPDIR}/map.820.4010.X061.xml
	${TRANS} -o 820.seg.html map_seg.xsl ${MAPDIR}/map.820.4010.X061.xml

835.seg.html: ${MAPDIR}/map.835.4010.X091.xml
	${TRANS} -o 835.seg.html map_seg.xsl ${MAPDIR}/map.835.4010.X091.xml

837.X096.seg.html: ${MAPDIR}/map.837.4010.X096.xml
	${TRANS} -o 837.X096.seg.html map_seg.xsl ${MAPDIR}/map.837.4010.X096.xml

837.X097.seg.html: ${MAPDIR}/map.837.4010.X097.xml
	${TRANS} -o 837.X097.seg.html map_seg.xsl ${MAPDIR}/map.837.4010.X097.xml

837.X098.seg.html: ${MAPDIR}/map.837.4010.X098.xml
	${TRANS} -o 837.X098.seg.html map_seg.xsl ${MAPDIR}/map.837.4010.X098.xml

270.loop.html: ${MAPDIR}/map.270.4010.X092.xml
	${TRANS} -o 270.loop.html loop.xsl ${MAPDIR}/map.270.4010.X092.xml

271.loop.html: ${MAPDIR}/map.271.4010.X092.xml
	${TRANS} -o 271.loop.html loop.xsl ${MAPDIR}/map.271.4010.X092.xml

276.loop.html: ${MAPDIR}/map.276.4010.X093.xml
	${TRANS} -o 276.loop.html loop.xsl ${MAPDIR}/map.276.4010.X093.xml

277.loop.html: ${MAPDIR}/map.277.4010.X093.xml
	${TRANS} -o 277.loop.html loop.xsl ${MAPDIR}/map.277.4010.X093.xml

278.loop.27.html: ${MAPDIR}/map.278.4010.X094.27.xml
	${TRANS} -o 278.loop.27.html loop.xsl ${MAPDIR}/map.278.4010.X094.27.xml

278.loop.html: ${MAPDIR}/map.278.4010.X094.xml
	${TRANS} -o 278.loop.html loop.xsl ${MAPDIR}/map.278.4010.X094.xml

820.loop.html: ${MAPDIR}/map.820.4010.X061.xml
	${TRANS} -o 820.loop.html loop.xsl ${MAPDIR}/map.820.4010.X061.xml

835.loop.html: ${MAPDIR}/map.835.4010.X091.xml
	${TRANS} -o 835.loop.html loop.xsl ${MAPDIR}/map.835.4010.X091.xml

837.X096.loop.html: ${MAPDIR}/map.837.4010.X096.xml
	${TRANS} -o 837.X096.loop.html loop.xsl ${MAPDIR}/map.837.4010.X096.xml

837.X097.loop.html: ${MAPDIR}/map.837.4010.X097.xml
	${TRANS} -o 837.X097.loop.html loop.xsl ${MAPDIR}/map.837.4010.X097.xml

837.X098.loop.html: ${MAPDIR}/map.837.4010.X098.xml
	${TRANS} -o 837.X098.loop.html loop.xsl ${MAPDIR}/map.837.4010.X098.xml


270.seg.html 271.seg.html 276.seg.html 277.seg.html 278.seg.27.html 278.seg.html 820.seg.html 835.seg.html 837.X096.seg.html 837.X097.seg.html 837.X098.seg.html: map_seg.xsl

270.sum.html 271.sum.html 276.sum.html 277.sum.html 278.sum.27.html 278.sum.html 820.sum.html 835.sum.html 837.X096.sum.html 837.X097.sum.html 837.X098.sum.html: map_sum.xsl

270.loop.html 271.loop.html 276.loop.html 277.loop.html 278.loop.27.html 278.loop.html 820.loop.html 835.loop.html 837.X096.loop.html 837.X097.loop.html 837.X098.loop.html: loop.xsl
