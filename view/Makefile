# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#
# #Id$

TRANS=/usr/local/bin/sabcmd
MAP=../map

all: 270 271 276 277 820 835 837I 837P 837D codes

270: 270.sum.html 270.seg.html

271: 271.sum.html 271.seg.html

276: 276.sum.html 276.seg.html

277: 277.sum.html 277.seg.html

278: 278.sum.27.html 278.seg.27.html 278.sum.html 278.seg.html

820: 820.sum.html 820.seg.html

835: 835.sum.html 835.seg.html

837I: 837.X096.sum.html 837.X096.seg.html

837D: 837.X097.sum.html 837.X097.seg.html

837P: 837.X098.sum.html 837.X098.seg.html

codes: codes.html

codes.html: ${MAP}/codes.xml
	${TRANS} -m ../codes.xsl ${MAP}/codes.xml codes.html

270.sum.html: ${MAP}/map.270.4010.X092.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.270.4010.X092.xml 270.sum.html

271.sum.html: ${MAP}/map.271.4010.X092.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.271.4010.X092.xml 271.sum.html

276.sum.html: ${MAP}/map.276.4010.X093.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.276.4010.X093.xml 276.sum.html

277.sum.html: ${MAP}/map.277.4010.X093.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.277.4010.X093.xml 277.sum.html

278.sum.27.html: ${MAP}/map.278.4010.X094.27.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.278.4010.X094.27.xml 278.sum.27.html

278.sum.html: ${MAP}/map.278.4010.X094.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.278.4010.X094.xml 278.sum.html

820.sum.html: ${MAP}/map.820.4010.X061.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.820.4010.X061.xml 820.sum.html

835.sum.html: ${MAP}/map.835.4010.X091.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.835.4010.X091.xml 835.sum.html

837.X096.sum.html: ${MAP}/map.837.4010.X096.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.837.4010.X096.xml 837.X096.sum.html

837.X097.sum.html: ${MAP}/map.837.4010.X097.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.837.4010.X097.xml 837.X097.sum.html

837.X098.sum.html: ${MAP}/map.837.4010.X098.xml
	${TRANS} -m ../map_sum.xsl ${MAP}/map.837.4010.X098.xml 837.X098.sum.html

270.seg.html: ${MAP}/map.270.4010.X092.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.270.4010.X092.xml 270.seg.html

271.seg.html: ${MAP}/map.271.4010.X092.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.271.4010.X092.xml 271.seg.html

276.seg.html: ${MAP}/map.276.4010.X093.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.276.4010.X093.xml 276.seg.html

277.seg.html: ${MAP}/map.277.4010.X093.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.277.4010.X093.xml 277.seg.html

278.seg.27.html: ${MAP}/map.278.4010.X094.27.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.278.4010.X094.27.xml 278.seg.27.html

278.seg.html: ${MAP}/map.278.4010.X094.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.278.4010.X094.xml 278.seg.html

820.seg.html: ${MAP}/map.820.4010.X061.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.820.4010.X061.xml 820.seg.html

835.seg.html: ${MAP}/map.835.4010.X091.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.835.4010.X091.xml 835.seg.html

837.X096.seg.html: ${MAP}/map.837.4010.X096.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.837.4010.X096.xml 837.X096.seg.html

837.X097.seg.html: ${MAP}/map.837.4010.X097.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.837.4010.X097.xml 837.X097.seg.html

837.X098.seg.html: ${MAP}/map.837.4010.X098.xml
	${TRANS} -m ../map_seg.xsl ${MAP}/map.837.4010.X098.xml 837.X098.seg.html

