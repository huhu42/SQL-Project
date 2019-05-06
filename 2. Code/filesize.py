import os

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

print getSize("toronto_audit.osm")