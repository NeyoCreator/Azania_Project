import json

#READ DATA
with open('backend_data/sample.json') as f:
   data = json.load(f)

#OBTAIN AND APPEND NEW DATA
new_data = {"icon_url":"https://i.pinimg.com/236x/d3/f2/b6/d3f2b6886f400ec0f453973d3c86f03e.jpg", "name":"JayZ", "pick_location":"Johannesburg Cental","destination":"Sandton City"}
data.append(new_data)

#WRITE TO JSON FILE
with open('backend_data/sample.json', 'w') as json_file:
    json.dump(data, json_file, 
                        indent=4,  
                        separators=(',',': '))