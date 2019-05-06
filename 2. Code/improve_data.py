"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "toronto.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcode = re.compile(r'[A-z]\d[A-z]\s?\d[A-z]\d')


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "Way", "Acres","Campanile", "Circle", "Circuit","Crestway", "Crossing",
            "Esplanade", "Fernway", "Gardens", "Gate", "Grove", "Heights", "Hill", "Highway", "Hillway", "Kingsway",
            "Line", "Mall", "Mews", "Millway", "Park", "Path", "Pathway", "Queensway", "Ridge", "Terrace", "Westway"]

# UPDATE THIS VARIABLE
mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "avenue": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Crest": "Crescent",
            "Ct": "Court",
            "dr": "Drive",
            "Dr": "Drive",
            "E": "East",
            "E.": "East",
            "Lane,": "Lane",
            "Ln": "Lane",
            "N": "North",
            "Pkwy": "Parkway",
            "Pl": "Place",
            "Rd": "Road",
            "rd": "Road",
            "St": "Street",
            "St.": "Street",
            "STREET": "Street",
            "street": "Street",
            "Terace": "Terrace",
            "Trl": "Trail",
            "W": "West",
            "W.": "West",
            "west": "West",
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            return True
    return False


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#postcode
def update_postcode(post_code):

    m = postcode.match(post_code)
    if m:
        if " " not in post_code:
            post_code = post_code [:3]+" "+post_code[3:]
        post_code = post_code.upper()
    return post_code

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#city
cityof = re.compile('of',re.IGNORECASE )
first= re.compile(';')
second = re.compile(',')
township = re.compile('Township')
bracket = re.compile(r'\(')

def update_city(city):

    m = cityof.search(city)
    n = first.search(city)
    o = second.search(city)
    t = township.search(city)
    b = bracket.search(city)
# if the city name starts with township, then only take the part after "township of"
    if t:
        city = city[12:].title()
# if the city name has bracket "(", then only take what's inside the bracket

    elif b:
        city = city.split("(")[1][:-1].title()
# if the city name has ";", then only take the part
    elif n:
        city = city.split(";")[1][8:].title()
# if the city name has "," in it, then only take the first part before the ","
    elif o:
        city = city.split(",")[0].title()
# if the city name has "city/town of" in it, then only take the part after

    elif m:
        city = city[8:].title()
# correct mis-spelled
    elif city == "Etoicoke":
        city = "Etobicoke"
# correct incorrect city torontoitalian
    elif city =="Torontoitalian":
        city = "Toronto"
    return city



def is_city(elem):
    return (elem.attrib['k'] == "addr:city")


#update the file

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    tree = ET.parse(osm_file)

    for elem in list(tree.iter()):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if audit_street_type(street_types, tag.attrib['v']):
                        tag.attrib["v"]=update_name(tag.attrib["v"], mapping)
                if is_postcode(tag):
                    tag.attrib["v"] = update_postcode(tag.attrib['v'])
                if is_city(tag):
                    tag.attrib['v'] = tag.attrib['v'].title()
                    tag.attrib["v"] = update_city(tag.attrib['v'])

    tree.write(osmfile[:osmfile.find('.osm')] + '_audit.osm')
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)

    return name


def test():

    st_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types))

    #for st_type, ways in st_types.iteritems():
        #for name in ways:
            #better_name = update_name(name, mapping)
            #print name, "=>", better_name


if __name__ == '__main__':
    audit(OSMFILE)