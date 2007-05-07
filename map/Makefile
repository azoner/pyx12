# Builds the html representations of the map summaries and segment detail, as well as supporting files.
# This file is part of the pyX12 project.
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#
# Uses the xlstproc processor - part of the the Gnome libxlst library
#
# $Id$

XSLT=/usr/local/bin/xsltproc
MAPDIR=.
OUTPUTDIR=../../pyx12-web/doc/maps
MAPS=270 271 276 277 278 820 835 837D 837I 837P 841 834 997

LINT=/usr/local/bin/xmllint

all: ${MAPS} codes dataele

270: 270.A1.sum.html 270.A1.seg.html 270.A1.loop.html

271: 271.A1.sum.html 271.A1.seg.html 271.A1.loop.html

276: 276.A1.sum.html 276.A1.seg.html 276.A1.loop.html

277: 277.A1.sum.html 277.A1.seg.html 277.A1.loop.html

278: 278.A1.sum.27.html 278.A1.seg.27.html 278.A1.sum.html 278.A1.seg.html 278.A1.loop.html 278.A1.loop.27.html

820: 820.A1.sum.html 820.A1.seg.html 820.A1.loop.html

834: 834.A1.sum.html 834.A1.seg.html 834.A1.loop.html

835: 835.A1.sum.html 835.A1.seg.html 835.A1.loop.html

837I: 837.X096.A1.sum.html 837.X096.A1.seg.html 837.X096.A1.loop.html

837D: 837.X097.A1.sum.html 837.X097.A1.seg.html 837.X097.A1.loop.html

837P: 837.X098.A1.sum.html 837.X098.A1.seg.html 837.X098.A1.loop.html

841: 841.XXXC.sum.html 841.XXXC.seg.html 841.XXXC.loop.html

997: 997.sum.html 997.seg.html 997.loop.html

codes: codes.html 

codes.html: ${MAPDIR}/codes.xml
	${XSLT} -o ${OUTPUTDIR}/codes.html codes.xsl ${MAPDIR}/codes.xml

codes.html: codes.xsl

dataele: dataele.html 

dataele.html: ${MAPDIR}/dataele.xml
	${XSLT} -o ${OUTPUTDIR}/dataele.html dataele.xsl ${MAPDIR}/dataele.xml

dataele.html: dataele.xsl

841.XXXC.loop.html: ${MAPDIR}/841.4010.XXXC.xml
	${XSLT} -o ${OUTPUTDIR}/841.XXXC.loop.html loop.xsl ${MAPDIR}/841.4010.XXXC.xml

997.loop.html: ${MAPDIR}/997.4010.xml
	${XSLT} -o ${OUTPUTDIR}/997.loop.html loop.xsl ${MAPDIR}/997.4010.xml

841.XXXC.sum.html: ${MAPDIR}/841.4010.XXXC.xml
	${XSLT} -o ${OUTPUTDIR}/841.XXXC.sum.html map_sum.xsl ${MAPDIR}/841.4010.XXXC.xml

997.sum.html: ${MAPDIR}/997.4010.xml
	${XSLT} -o ${OUTPUTDIR}/997.sum.html map_sum.xsl ${MAPDIR}/997.4010.xml

841.XXXC.seg.html: ${MAPDIR}/841.4010.XXXC.xml
	${XSLT} -o ${OUTPUTDIR}/841.XXXC.seg.html map_seg.xsl ${MAPDIR}/841.4010.XXXC.xml

997.seg.html: ${MAPDIR}/997.4010.xml
	${XSLT} -o ${OUTPUTDIR}/997.seg.html map_seg.xsl ${MAPDIR}/997.4010.xml

# A1 Versions
270.A1.sum.html: ${MAPDIR}/270.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/270.A1.sum.html map_sum.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.sum.html: ${MAPDIR}/271.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/271.A1.sum.html map_sum.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.sum.html: ${MAPDIR}/276.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/276.A1.sum.html map_sum.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.sum.html: ${MAPDIR}/277.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/277.A1.sum.html map_sum.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.sum.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.sum.27.html map_sum.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.sum.html: ${MAPDIR}/278.4010.X094.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.sum.html map_sum.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.sum.html: ${MAPDIR}/820.4010.X061.A1.xml
	${XSLT} -o ${OUTPUTDIR}/820.A1.sum.html map_sum.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.sum.html: ${MAPDIR}/834.4010.X095.A1.xml
	${XSLT} -o ${OUTPUTDIR}/834.A1.sum.html map_sum.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.sum.html: ${MAPDIR}/835.4010.X091.A1.xml
	${XSLT} -o ${OUTPUTDIR}/835.A1.sum.html map_sum.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.sum.html: ${MAPDIR}/837.4010.X096.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X096.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.sum.html: ${MAPDIR}/837.4010.X097.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X097.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.sum.html: ${MAPDIR}/837.4010.X098.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X098.A1.sum.html map_sum.xsl ${MAPDIR}/837.4010.X098.A1.xml

270.A1.seg.html: ${MAPDIR}/270.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/270.A1.seg.html map_seg.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.seg.html: ${MAPDIR}/271.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/271.A1.seg.html map_seg.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.seg.html: ${MAPDIR}/276.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/276.A1.seg.html map_seg.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.seg.html: ${MAPDIR}/277.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/277.A1.seg.html map_seg.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.seg.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.seg.27.html map_seg.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.seg.html: ${MAPDIR}/278.4010.X094.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.seg.html map_seg.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.seg.html: ${MAPDIR}/820.4010.X061.A1.xml
	${XSLT} -o ${OUTPUTDIR}/820.A1.seg.html map_seg.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.seg.html: ${MAPDIR}/834.4010.X095.A1.xml
	${XSLT} -o ${OUTPUTDIR}/834.A1.seg.html map_seg.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.seg.html: ${MAPDIR}/835.4010.X091.A1.xml
	${XSLT} -o ${OUTPUTDIR}/835.A1.seg.html map_seg.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.seg.html: ${MAPDIR}/837.4010.X096.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X096.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.seg.html: ${MAPDIR}/837.4010.X097.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X097.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.seg.html: ${MAPDIR}/837.4010.X098.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X098.A1.seg.html map_seg.xsl ${MAPDIR}/837.4010.X098.A1.xml

270.A1.loop.html: ${MAPDIR}/270.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/270.A1.loop.html loop.xsl ${MAPDIR}/270.4010.X092.A1.xml

271.A1.loop.html: ${MAPDIR}/271.4010.X092.A1.xml
	${XSLT} -o ${OUTPUTDIR}/271.A1.loop.html loop.xsl ${MAPDIR}/271.4010.X092.A1.xml

276.A1.loop.html: ${MAPDIR}/276.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/276.A1.loop.html loop.xsl ${MAPDIR}/276.4010.X093.A1.xml

277.A1.loop.html: ${MAPDIR}/277.4010.X093.A1.xml
	${XSLT} -o ${OUTPUTDIR}/277.A1.loop.html loop.xsl ${MAPDIR}/277.4010.X093.A1.xml

278.A1.loop.27.html: ${MAPDIR}/278.4010.X094.27.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.loop.27.html loop.xsl ${MAPDIR}/278.4010.X094.27.A1.xml

278.A1.loop.html: ${MAPDIR}/278.4010.X094.A1.xml
	${XSLT} -o ${OUTPUTDIR}/278.A1.loop.html loop.xsl ${MAPDIR}/278.4010.X094.A1.xml

820.A1.loop.html: ${MAPDIR}/820.4010.X061.A1.xml
	${XSLT} -o ${OUTPUTDIR}/820.A1.loop.html loop.xsl ${MAPDIR}/820.4010.X061.A1.xml

834.A1.loop.html: ${MAPDIR}/834.4010.X095.A1.xml
	${XSLT} -o ${OUTPUTDIR}/834.A1.loop.html loop.xsl ${MAPDIR}/834.4010.X095.A1.xml

835.A1.loop.html: ${MAPDIR}/835.4010.X091.A1.xml
	${XSLT} -o ${OUTPUTDIR}/835.A1.loop.html loop.xsl ${MAPDIR}/835.4010.X091.A1.xml

837.X096.A1.loop.html: ${MAPDIR}/837.4010.X096.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X096.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X096.A1.xml

837.X097.A1.loop.html: ${MAPDIR}/837.4010.X097.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X097.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X097.A1.xml

837.X098.A1.loop.html: ${MAPDIR}/837.4010.X098.A1.xml
	${XSLT} -o ${OUTPUTDIR}/837.X098.A1.loop.html loop.xsl ${MAPDIR}/837.4010.X098.A1.xml

841.XXXC.seg.html 997.seg.html 270.A1.seg.html 271.A1.seg.html 276.A1.seg.html 277.A1.seg.html 278.A1.seg.27.html 278.A1.seg.html 820.A1.seg.html 834.A1.seg.html 835.A1.seg.html 837.X096.A1.seg.html 837.X097.A1.seg.html 837.X098.A1.seg.html: map_seg.xsl

841.XXXC.sum.html 997.sum.html 270.A1.sum.html 271.A1.sum.html 276.A1.sum.html 277.A1.sum.html 278.A1.sum.27.html 278.A1.sum.html 820.A1.sum.html 834.A1.sum.html 835.A1.sum.html 837.X096.A1.sum.html 837.X097.A1.sum.html 837.X098.A1.sum.html: map_sum.xsl

841.XXXC.loop.html 997.loop.html 270.A1.loop.html 271.A1.loop.html 276.A1.loop.html 277.A1.loop.html 278.A1.loop.27.html 278.A1.loop.html 820.A1.loop.html 834.A1.loop.html 835.A1.loop.html 837.X096.A1.loop.html 837.X097.A1.loop.html 837.X098.A1.loop.html: loop.xsl


lint: 
	${LINT} --format -o 270.4010.X092.A1.xml 270.4010.X092.A1.xml
	${LINT} --format -o 271.4010.X092.A1.xml 271.4010.X092.A1.xml 
	${LINT} --format -o 276.4010.X093.A1.xml 276.4010.X093.A1.xml
	${LINT} --format -o 277.4010.X093.A1.xml 277.4010.X093.A1.xml
	${LINT} --format -o 278.4010.X094.27.A1.xml 278.4010.X094.27.A1.xml
	${LINT} --format -o 278.4010.X094.A1.xml 278.4010.X094.A1.xml
	${LINT} --format -o 820.4010.X061.A1.xml 820.4010.X061.A1.xml
	${LINT} --format -o 834.4010.X095.A1.xml 834.4010.X095.A1.xml
	${LINT} --format -o 835.4010.X091.A1.xml 835.4010.X091.A1.xml
	${LINT} --format -o 837.4010.X096.A1.xml 837.4010.X096.A1.xml
	${LINT} --format -o 837.4010.X097.A1.xml 837.4010.X097.A1.xml
	${LINT} --format -o 837.4010.X098.A1.xml 837.4010.X098.A1.xml
	${LINT} --format -o 277.4020.X104.xml 277.4020.X104.xml
	${LINT} --format -o 841.4010.XXXC.xml 841.4010.XXXC.xml
	${LINT} --format -o 997.4010.xml 997.4010.xml
	${LINT} --format -o codes.xml codes.xml
	${LINT} --format -o comp_test.xml comp_test.xml
	${LINT} --format -o maps.xml maps.xml
	${LINT} --format -o x12.control.00401.xml x12.control.00401.xml
