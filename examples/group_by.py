"""
Example of group_by()
"""
from pyjsonq.query import JsonQ

e1 = JsonQ("./data.json").at("products").group_by("price").get()

print("result", e1)
