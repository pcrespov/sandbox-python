from json_logic import eval_json_logic

res = eval_json_logic({"==": [1, 1]})
print(f"{res=}")

rules = {
    "and": [{"<": [{"var": "temp"}, 110]}, {"==": [{"var": "pie.filling"}, "apple"]}]
}

data = {"temp": 100, "pie": {"filling": "apple"}}

eval_json_logic(rules, data)

print(f"{rules=}, {data=}, {res=}")

# TODO: schema for json-logic ??
# TODO: pie.*.filling?
# TODO: pydantic has also these extended paths for include/exclude... 