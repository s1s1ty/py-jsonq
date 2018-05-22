"""
Example of sum()
"""
from pyjsonq import JsonQ

e1 = JsonQ("./data.json").at("users.5.visits").sum("year")

print("result", e1)
