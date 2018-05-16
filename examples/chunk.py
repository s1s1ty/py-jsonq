"""
Example of chunk()
"""
from pyjsonq.query import JsonQ

e1 = JsonQ("./data.json").at("users").where("location", "=", "Barisal").chunk(2)

print("result", e1)