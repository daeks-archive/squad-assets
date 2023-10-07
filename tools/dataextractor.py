import json
import os
import sys
import time
import traceback

dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
    # Get Data from LayerFile provided by SquadWikiPipeline Tool
    layers: json = json.load(open(dir_path+"\\layers.json"))
    maplistdata = createMapList(layers)
    # save as maplist.txt
    with open("maplist.txt", "w") as f:
        for map in maplistdata:
            f.write(map + "\n")
    #prepare mapdata.json
    mapdata = createMapDataJSON(layers)
    print(mapdata)


def createMapList(layers:json)-> [str]:        # Create maplist.json data
    result = []

    for map in layers["Maps"]:
        result.append(map["levelName"])
    return result

def createMapDataJSON(layers:json)-> json:        # Create mapdata.json data
    #do we need this or are we using the layers.json?
    
    result: json = {}

    for map in layers["Maps"]:

        teams = []    # Create teams array instead of using keys
        for key in map:
            if key.startswith("team"):
                team_data = map[key]
                team_data["name"] = key
                #might add Team Tag here
                teams.append(team_data)
        


        result[map["levelName"]] = {
            "name": map["Name"],
            "raw": map["rawName"],
            "level": map["levelName"],
            "map": map["mapName"],
            "mode": map["gamemode"],
            "layer": map["layerVersion"],
            #plugin?
            "size":  str(map["mapSize"]).split(" ")[0],
            "sizeUnit": str(map["mapSize"]).split(" ")[1],
            "weather": map["lighting"] if "lighting" in map else "",
            #commander can be different for each team // removed
            "teams": teams,
            "flags": map["Flag"] if "Flag" in map else [],
        }
    return result

if __name__ == "__main__":
    main()

