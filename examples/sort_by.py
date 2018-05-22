"""
Example of sort_by()
"""
from pyjsonq import JsonQ

e1 = JsonQ("./data.json").at("products").sort_by("id", "desc").get()

print("result", e1)
