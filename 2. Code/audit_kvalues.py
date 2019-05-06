#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re


osm_file = open("toronto_audit.osm", "r")
#street_type_re = re.compile(r'\S+\.?$')
ktype = defaultdict(int)

#ef audit_postcode(post_codes):
   # m = street_type_re.search(street_name)
    #if post_code not in post_codes:
       # street_type = m.group()
   # else:
        #post_codes[post_code] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)


def audit(kvalue):
    for event, elem in ET.iterparse(osm_file):
        if (elem.tag =="tag") and (elem.attrib['k']==kvalue):
            ktype[elem.attrib['v']] += 1
    print_sorted_dict(ktype)
    osm_file.close()

if __name__ == '__main__':
    audit("addr:street")
    audit('addr:postcode')
    audit('addr:city')

