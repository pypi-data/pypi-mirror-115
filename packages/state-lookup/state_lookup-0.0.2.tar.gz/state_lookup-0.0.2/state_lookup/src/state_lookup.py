import ast, pickle
with open("./city-state-map.pkl","rb") as f:
	lookup = pickle.load(f)

lookup = ast.literal_eval(lookup)

def return_state(city,mapping_dict=lookup):
    try:
        if "," in city:
            city,state = list(map(lambda x:x.strip(),city.split(",")))
            city = f"{city.capitalize()}, {state.upper()}"
            return city
        src_list = mapping_dict[city[0].lower()]
        lower_list = list(map(lambda x:x.lower(),mapping_dict[city[0].lower()]))
        found = []
        for j,i in enumerate(lower_list):
            if f"{city.lower()}" in i.split(", "):
                found.append(src_list[j])
        if len(found) > 1:
            return city.capitalize()
        else:
            return found[0]
    except:
        cities = list(map(lambda x:x.capitalize(),city.split()))
        if len(cities) > 1:
            city = " ".join(cities)
        else:
            city = cities[0]
        return city