#!/bin/sh
# Build the Segment and Loop Summary HTML Views.  Uses the Sabletron XSLT engine.
TRANS=/usr/local/bin/sabcmd


${TRANS} -m ./map_sum.xsl map/map.270.4010.X092.xml view/270.sum.html
${TRANS} -m ./map_sum.xsl map/map.271.4010.X092.xml view/271.sum.html
${TRANS} -m ./map_sum.xsl map/map.276.4010.X093.xml view/276.sum.html
${TRANS} -m ./map_sum.xsl map/map.277.4010.X093.xml view/277.sum.html
${TRANS} -m ./map_sum.xsl map/map.278.4010.X094.27.xml view/278.sum.27.html
${TRANS} -m ./map_sum.xsl map/map.278.4010.X094.xml view/278.sum.html
${TRANS} -m ./map_sum.xsl map/map.820.4010.X061.xml view/820.sum.html
${TRANS} -m ./map_sum.xsl map/map.835.4010.X091.xml view/835.sum.html
${TRANS} -m ./map_sum.xsl map/map.837.4010.X096.xml view/837.X096.sum.html
${TRANS} -m ./map_sum.xsl map/map.837.4010.X097.xml view/837.X097.sum.html
${TRANS} -m ./map_sum.xsl map/map.837.4010.X098.xml view/837.X098.sum.html

${TRANS} -m ./map_seg.xsl map/map.270.4010.X092.xml view/270.seg.html
${TRANS} -m ./map_seg.xsl map/map.271.4010.X092.xml view/271.seg.html
${TRANS} -m ./map_seg.xsl map/map.276.4010.X093.xml view/276.seg.html
${TRANS} -m ./map_seg.xsl map/map.277.4010.X093.xml view/277.seg.html
${TRANS} -m ./map_seg.xsl map/map.278.4010.X094.27.xml view/278.seg.27.html
${TRANS} -m ./map_seg.xsl map/map.278.4010.X094.xml view/278.seg.html
${TRANS} -m ./map_seg.xsl map/map.820.4010.X061.xml view/820.seg.html
${TRANS} -m ./map_seg.xsl map/map.835.4010.X091.xml view/835.seg.html
${TRANS} -m ./map_seg.xsl map/map.837.4010.X096.xml view/837.X096.seg.html
${TRANS} -m ./map_seg.xsl map/map.837.4010.X097.xml view/837.X097.seg.html
${TRANS} -m ./map_seg.xsl map/map.837.4010.X098.xml view/837.X098.seg.html

