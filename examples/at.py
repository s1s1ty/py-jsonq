"""
Example of at()
"""
from pyjsonq.query import JsonQ

qe = JsonQ("./data.json").at("users").where("id", "<", 3).get()

print("result", qe)
