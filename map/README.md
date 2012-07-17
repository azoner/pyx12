# X12 Mapping rules and Notes

Add reference to maps.xml - ensure xid == abbr
834 - fix 2700/2710/LS/LE struct

837 - Copy 2300 to be a child of both 2000B and 2000C

Loops inherit the IG usage of their first child.  The first child is then required.

Move ST and SE segments to be a direct child of ST_LOOP

Is the map expecting fixed wrapper loops?  HEADER, DETAIL, FOOTER

For the 5010 maps, move single child elements (name, pos, id, ...) to attributes.  Will use a modified schema: map.v2.xsd.






