# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# #Id$

TRANS=/usr/local/bin/xsltproc
MAPDIR=../map
MAPS=270 271 276 277 278 820 835 837D 837I 837P 841 834 997

all: ${MAPS} codes

270: 270.sum.html 270.seg.html 270.loop.html 270.A1.sum.html 270.A1.seg.html 270.A1.loop.html

271: 271.sum.html 271.seg.html 271.loop.html 271.A1.sum.html 271.A1.seg.html 271.A1.loop.html

276: 276.sum.html 276.seg.html 276.loop.html 276.A1.sum.html 276.A1.seg.html 276.A1.loop.html

277: 277.sum.html 277.seg.html 277.loop.html 277.A1.sum.html 277.A1.seg.html 277.A1.loop.html

278: 278.sum.27.html 278.seg.27.html 278.sum.html 278.seg.html 278.loop.html 278.loop.27.html 278.A1.sum.27.html 278.A1.seg.27.html 278.A1.sum.html 278.A1.seg.html 278.A1.loop.html 278.A1.loop.27.html

820: 820.sum.html 820.seg.html 820.loop.html 820.A1.sum.html 820.A1.seg.html 820.A1.loop.html

834: 834.A1.sum.html 834.A1.seg.html 834.A1.loop.html

835: 835.sum.html 835.seg.html 835.loop.html 835.A1.sum.html 835.A1.seg.html 835.A1.loop.html

#837: 837I 837D 837P

837I: 837.X096.sum.html 837.X096.seg.html 837.X096.loop.html 837.X096.A1.sum.html 837.X096.A1.seg.html 837.X096.A1.loop.html

837D: 837.X097.sum.html 837.X097.seg.html 837.X097.loop.html 837.X097.A1.sum.html 837.X097.A1.seg.html 837.X097.A1.loop.html

837P: 837.X098.sum.html 837.X098.seg.html 837.X098.loop.html 837.X098.A1.sum.html 837.X098.A1.seg.html 837.X098.A1.loop.html

841: 841.XXXC.sum.html 841.XXXC.seg.html 841.XXXC.loop.html

997: 997.sum.html 997.seg.html 997.loop.html

codes: codes.html 

codes.html: ${MAPDIR}/codes.xml
	${TRANS} -o codes.html codes.xsl ${MAPDIR}/codes.xml

codes.html: codes.xsl

270.sum.html: ${MAPDIR}/270.4010.X092.xml
	${TRANS} -o 270.sum.html map_sum.xsl ${MAPDIR}/270.4010.X092.xml

271.sum.html: ${MAPDIR}/271.4010.X092.xml
	${TRANS} -o 271.sum.html map_sum.xsl ${MAPDIR}/271.4010.X092.xml

276.sum.html: ${MAPDIR}/276.4010.X093.xml
	${TRANS} -o 276.sum.html map_sum.xsl ${MAPDIR}/276.4010.X093.xml

277.sum.html: ${MAPDIR}/277.4010.X093.xml
	${TRANS} -o 277.sum.html map_sum.xsl ${MAPDIR}/277.4010.X093.xml

278.sum.27.html: ${MAPDIR}/278.4010.X094.27.xml
	${TRANS} -o 278.sum.27.html map_sum.xsl ${MAPDIR}/278.4010.X094.27.xml

278.sum.html: ${MAPDIR}/278.4010.X094.xml
	${TRANS} -o 278.sum.html map_sum.xsl ${MAPDIR}/278.4010.X094.xml

820.sum.html: ${MAPDIR}/820.4010.X061.xml
	${TRANS} -o 820.sum.html map_sum.xsl ${MAPDIR}/820.4010.X061.xml

835.sum.html: ${MAPDIR}/835.4010.X091.xml
	${TRANS} -o 835.sum.html map_sum.xsl ${MAPDIR}/835.4010.X091.xml

837.X096.sum.html: ${MAPDIR}/837.4010.X096.xml
	${TRANS} -o 837.X096.sum.html map_sum.xsl ${MAPDIR}/837.4010.X096.xml

837.X097.sum.html: ${MAPDIR}/837.4010.X097.xml
	${TRANS} -o 837.X097.sum.html map_sum.xsl ${MAPDIR}/837.4010.X097.xml

837.X098.sum.html: ${MAPDIR}/837.4010.X098.xml
	${TRANS} -o 837.X098.sum.html map_sum.xsl ${MAPDIR}/837.4010.X098.xml

841.XXXC.sum.html: ${MAPDIR}/841.4010.XXXC.xml
	${TRANS} -o 841.XXXC.sum.html map_sum.xsl ${MAPDIR}/841.4010.XXXC.xml

997.sum.html: ${MAPDIR}/997.4010.xml
	${TRANS} -o 997.sum.html map_sum.xsl ${MAPDIR}/997.4010.xml

270.seg.html: ${MAPDIR}/270.4010.X092.xml
	${TRANS} -o 270.seg.html map_seg.xsl ${MAPDIR}/270.4010.X092.xml

271.seg.html: ${MAPDIR}/271.4010.X092.xml
	${TRANS} -o 271.seg.html map_seg.xsl ${MAPDIR}/271.4010.X092.xml

276.seg.html: ${MAPDIR}/276.4010.X093.xml
	${TRANS} -o 276.seg.html map_seg.xsl ${MAPDIR}/276.4010.X093.xml

277.seg.html: ${MAPDIR}/277.4010.X093.xml
	${TRANS} -o 277.seg.html map_seg.xsl ${MAPDIR}/277.4010.X093.xml

278.seg.27.html: ${MAPDIR}/278.4010.X094.27.xml
	${TRANS} -o 278.seg.27.html map_seg.xsl ${MAPDIR}/278.4010.X094.27.xml

278.seg.html: ${MAPDIR}/278.4010.X094.xml
	${TRANS} -o 278.seg.html map_seg.xsl ${MAPDIR}/278.4010.X094.xml

820.seg.html: ${MAPDIR}/820.4010.X061.xml
	${TRANS} -o 820.seg.html map_seg.xsl ${MAPDIR}/820.4010.X061.xml

835.seg.html: ${MAPDIR}/835.4010.X091.xml
	${TRANS} -o 835.seg.html map_seg.xsl ${MAPDIR}/835.4010.X091.xml

837.X096.seg.html: ${MAPDIR}/837.4010.X096.xml
	${TRANS} -o 837.X096.seg.html map_seg.xsl ${MAPDIR}/837.4010.X096.xml

837.X097.seg.html: ${MAPDIR}/837.4010.X097.xml
	${TRANS} -o 837.X097.seg.html map_seg.xsl ${MAPDIR}/837.4010.X097.xml

837.X098.seg.html: ${MAPDIR}/837.4010.X098.xml
	${TRANS} -o 837.X098.seg.html map_seg.xsl ${MAPDIR}/837.4010.X098.xml

841.XXXC.seg.html: ${MAPDIR}/841.4010.XXXC.xml
	${TRANS} -o 841.XXXC.seg.html map_seg.xsl ${MAPDIR}/841.4010.XXXC.xml

997.seg.html: ${MAPDIR}/997.4010.xml
	${TRANS} -o 997.seg.html map_seg.xsl ${MAPDIR}/997.4010.xml

270.loop.html: ${MAPDIR}/270.4010.X092.xml
	${TRANS} -o 270.loop.html loop.xsl ${MAPDIR}/270.4010.X092.xml

271.loop.html: ${MAPDIR}/271.4010.X092.xml
	${TRANS} -o 271.loop.html loop.xsl ${MAPDIR}/271.4010.X092.xml

276.loop.html: ${MAPDIR}/276.4010.X093.xml
	${TRANS} -o 276.loop.html loop.xsl ${MAPDIR}/276.4010.X093.xml

277.loop.html: ${MAPDIR}/277.4010.X093.xml
	${TRANS} -o 277.loop.html loop.xsl ${MAPDIR}/277.4010.X093.xml

278.loop.27.html: ${MAPDIR}/278.4010.X094.27.xml
	${TRANS} -o 278.loop.27.html loop.xsl ${MAPDIR}/278.4010.X094.27.xml

278.loop.html: ${MAPDIR}/278.4010.X094.xml
	${TRANS} -o 278.loop.html loop.xsl ${MAPDIR}/278.4010.X094.xml

820.loop.html: ${MAPDIR}/820.4010.X061.xml
	${TRANS} -o 820.loop.html loop.xsl ${MAPDIR}/820.4010.X061.xml

835.loop.html: ${MAPDIR}/835.4010.X091.xml
	${TRANS} -o 835.loop.html loop.xsl ${MAPDIR}/835.4010.X091.xml

837.X096.loop.html: ${MAPDIR}/837.4010.X096.xml
	${TRANS} -o 837.X096.loop.html loop.xsl ${MAPDIR}/837.4010.X096.xml

837.X097.loop.html: ${MAPDIR}/837.4010.X097.xml
	${TRANS} -o 837.X097.loop.html loop.xsl ${MAPDIR}/837.4010.X097.xml

837.X098.loop.html: ${MAPDIR}/837.4010.X098.xml
	${TRANS} -o 837.X098.loop.html loop.xsl ${MAPDIR}/837.4010.X098.xml

841.XXXC.loop.html: ${MAPDIR}/841.4010.XXXC.xml
	${TRANS} -o 841.XXXC.loop.html loop.xsl ${MAPDIR}/841.4010.XXXC.xml

997.loop.html: ${MAPDIR}/997.4010.xml
	${TRANS} -o 997.loop.html loop.xsl ${MAPDIR}/997.4010.xml

# A1 Versions
270.A1.sum.html: ${MAPDIR}/270.4010.X092.A1.xml
	${TRANS} -o 270.A1.sum.html map_sum.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.sum.html: ${MAPDIR}/271.4010.X092.A1.xml
	${TRANS} -o 271.A1.sum.html map_sum.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.sum.html: ${MAPDIR}/276.4010.X093.A1.xml
	${TRANS} -o 276.A1.sum.html map_sum.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.sum.html: ${MAPDIR}/277.4010.X093.A1.xml
	${TRANS} -o 277.A1.sum.html map_sum.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.sum.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${TRANS} -o 278.A1.sum.27.html map_sum.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.sum.html: ${MAPDIR}/278.4010.X094.A1.xml
	${TRANS} -o 278.A1.sum.html map_sum.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.sum.html: ${MAPDIR}/820.4010.X061.A1.xml
	${TRANS} -o 820.A1.sum.html map_sum.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.sum.html: ${MAPDIR}/834.4010.X095.A1.xml
	${TRANS} -o 834.A1.sum.html map_sum.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.sum.html: ${MAPDIR}/835.4010.X091.A1.xml
	${TRANS} -o 835.A1.sum.html map_sum.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.sum.html: ${MAPDIR}/837.4010.X096.A1.xml
	${TRANS} -o 837.X096.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.sum.html: ${MAPDIR}/837.4010.X097.A1.xml
	${TRANS} -o 837.X097.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.sum.html: ${MAPDIR}/837.4010.X098.A1.xml
	${TRANS} -o 837.X098.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X098.A1.xml

270.A1.seg.html: ${MAPDIR}/270.4010.X092.A1.xml
	${TRANS} -o 270.A1.seg.html map_seg.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.seg.html: ${MAPDIR}/271.4010.X092.A1.xml
	${TRANS} -o 271.A1.seg.html map_seg.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.seg.html: ${MAPDIR}/276.4010.X093.A1.xml
	${TRANS} -o 276.A1.seg.html map_seg.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.seg.html: ${MAPDIR}/277.4010.X093.A1.xml
	${TRANS} -o 277.A1.seg.html map_seg.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.seg.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${TRANS} -o 278.A1.seg.27.html map_seg.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.seg.html: ${MAPDIR}/278.4010.X094.A1.xml
	${TRANS} -o 278.A1.seg.html map_seg.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.seg.html: ${MAPDIR}/820.4010.X061.A1.xml
	${TRANS} -o 820.A1.seg.html map_seg.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.seg.html: ${MAPDIR}/834.4010.X095.A1.xml
	${TRANS} -o 834.A1.seg.html map_seg.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.seg.html: ${MAPDIR}/835.4010.X091.A1.xml
	${TRANS} -o 835.A1.seg.html map_seg.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.seg.html: ${MAPDIR}/837.4010.X096.A1.xml
	${TRANS} -o 837.X096.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.seg.html: ${MAPDIR}/837.4010.X097.A1.xml
	${TRANS} -o 837.X097.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.seg.html: ${MAPDIR}/837.4010.X098.A1.xml
	${TRANS} -o 837.X098.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X098.A1.xml

270.A1.loop.html: ${MAPDIR}/270.4010.X092.A1.xml
	${TRANS} -o 270.A1.loop.html loop.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.loop.html: ${MAPDIR}/271.4010.X092.A1.xml
	${TRANS} -o 271.A1.loop.html loop.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.loop.html: ${MAPDIR}/276.4010.X093.A1.xml
	${TRANS} -o 276.A1.loop.html loop.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.loop.html: ${MAPDIR}/277.4010.X093.A1.xml
	${TRANS} -o 277.A1.loop.html loop.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.loop.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${TRANS} -o 278.A1.loop.27.html loop.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.loop.html: ${MAPDIR}/278.4010.X094.A1.xml
	${TRANS} -o 278.A1.loop.html loop.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.loop.html: ${MAPDIR}/820.4010.X061.A1.xml
	${TRANS} -o 820.A1.loop.html loop.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.loop.html: ${MAPDIR}/834.4010.X095.A1.xml
	${TRANS} -o 834.A1.loop.html loop.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.loop.html: ${MAPDIR}/835.4010.X091.A1.xml
	${TRANS} -o 835.A1.loop.html loop.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.loop.html: ${MAPDIR}/837.4010.X096.A1.xml
	${TRANS} -o 837.X096.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.loop.html: ${MAPDIR}/837.4010.X097.A1.xml
	${TRANS} -o 837.X097.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.loop.html: ${MAPDIR}/837.4010.X098.A1.xml
	${TRANS} -o 837.X098.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X098.A1.xml

270.seg.html 271.seg.html 276.seg.html 277.seg.html 278.seg.27.html 278.seg.html 820.seg.html 835.seg.html 837.X096.seg.html 837.X097.seg.html 837.X098.seg.html 841.XXXC.seg.html 997.seg.html 270.A1.seg.html 271.A1.seg.html 276.A1.seg.html 277.A1.seg.html 278.A1.seg.27.html 278.A1.seg.html 820.A1.seg.html 834.A1.seg.html 835.A1.seg.html 837.X096.A1.seg.html 837.X097.A1.seg.html 837.X098.A1.seg.html: map_seg.xsl

270.sum.html 271.sum.html 276.sum.html 277.sum.html 278.sum.27.html 278.sum.html 820.sum.html 835.sum.html 837.X096.sum.html 837.X097.sum.html 837.X098.sum.html 841.XXXC.sum.html 997.sum.html 270.A1.sum.html 271.A1.sum.html 276.A1.sum.html 277.A1.sum.html 278.A1.sum.27.html 278.A1.sum.html 820.A1.sum.html 834.A1.sum.html 835.A1.sum.html 837.X096.A1.sum.html 837.X097.A1.sum.html 837.X098.A1.sum.html: map_sum.xsl

270.loop.html 271.loop.html 276.loop.html 277.loop.html 278.loop.27.html 278.loop.html 820.loop.html 835.loop.html 837.X096.loop.html 837.X097.loop.html 837.X098.loop.html 841.XXXC.loop.html 997.loop.html 270.A1.loop.html 271.A1.loop.html 276.A1.loop.html 277.A1.loop.html 278.A1.loop.27.html 278.A1.loop.html 820.A1.loop.html 834.A1.loop.html 835.A1.loop.html 837.X096.A1.loop.html 837.X097.A1.loop.html 837.X098.A1.loop.html: loop.xsl
