import googlemaps
import requests

#TODO ne plus coder en dur la clée API et les facteurs d'émissions
#TODO refactoriser le code pour ne plus avoir 
def distance_emissions(start,end,mode):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {"origins": start, "destinations": end, "mode": mode, "key": api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # print(f"Type des données renvoyées : {type(data)}")
        # print(f"Données brutes : {data}")
        if data["status"] == "OK":
            #print(data["rows"][0]["elements"][0])
            if data["rows"][0]["elements"][0] == {'status' : 'NOT_FOUND'} or data["rows"][0]["elements"][0] == {'status' : 'ZERO_RESULTS'}:
                return "PROBLEM" 
            else:
                distance = data["rows"][0]["elements"][0]["distance"]["text"].split(" ")[0]
                if mode=="Electric engine car":
                    emissions = distance*0.103   
                    return distance,emissions
                elif mode=="Bus":
                     emissions = distance*0.113
                     return distance, emissions
                elif mode=="Combustion engine car":
                     emissions == distance*0.218
                     return distance, emissions
                elif mode=="Train":
                     emissions = distance*0.003
                     return distance, emissions
                else:
                     return "PROBLEM"
        else:
            print("Request failed.")
            print(response)
            return 'PROBLEM'
    else:
            print("Failed to make the request.")
            print(response)
            return 'PROBLEM'
