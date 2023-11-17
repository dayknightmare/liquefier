import json
import math
import sys


with open(sys.argv[1]) as f:
    js = json.loads(f.read())

    print(math.ceil(float(js["totals"]["percent_covered"])), end="")
