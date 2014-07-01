import json
import argparse
import re
import unicodedata

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--id")
parser.add_argument("--icon")
parser.add_argument("--point", dest="geometry", action="append_const", const="point")
parser.add_argument("--area", dest="geometry", action="append_const", const="area")
parser.add_argument("--line", dest="geometry", action="append_const", const="line")
parser.add_argument("--vertex", dest="geometry", action="append_const", const="vertex")
parser.add_argument("--tags", dest="tags", action="append", default=[])

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                     if unicodedata.category(c) != 'Mn')

def idify(name):
    name = strip_accents(name.lower())
    return re.sub("\W", "_", name)

def update(d1, d2):
    d1 = dict(d1)
    d1.update(d2)
    return d1


args = parser.parse_args()

args.id = args.id or idify(args.name)
args.icon = args.icon or idify(args.name)
args.geometry = args.geometry or []


json.dump({
    "icon": args.icon,
    "geometry": args.geometry,
    "terms": [],
    "tags": update({"kta": args.id}, args.tags),
    "name": args.name,
}, open("presets/kta/" + args.id + ".json", "w"), indent=2)
