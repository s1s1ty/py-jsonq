from pyjsonq.query import JsonQ

e1 = JsonQ("./data.json").at("users").where("id", ">", 3).where("location", "=", "Barisal").get()

print("result", e1)

e2 = JsonQ("./data.json").at("users").where("id", ">", 3).where("location", "=", "Barisal").get()

print("result", e2)
