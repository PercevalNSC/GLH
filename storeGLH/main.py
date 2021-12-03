import json
from GLHload import GLHinit

with open('2018_APRIL_2.json', 'r') as f : 
    dict = json.load(f)

glhload = GLHinit(dict)
glhload.glhinit()