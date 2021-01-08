import os
import pprint
import csv
import re
import json
from datetime import datetime

schema = None
with open('./tfschema.json') as f:
    schema = json.loads(f.read())

schematypes = schema['provider_schemas']['registry.terraform.io/hashicorp/aws']['resource_schemas'].keys()

tftypes = []
with open('./tftypes.txt') as f:
    for line in f.read().split("\n"):
        tftypes.append(line)

for schematype in schematypes:
    if schematype not in tftypes:
        print(schematype + " not in types")

for tftype in tftypes:
    if tftype not in schematypes:
        print(tftype + " not in schema")