from django.core.management.base import BaseCommand, CommandError
import requests
import googlemaps

class Command(BaseCommand):
    def api():

        # Remplacez 'YOUR_API_KEY' par votre clé API Google Maps
        gmaps = googlemaps.Client(key='AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk')

        directions_result = gmaps.directions("Sydney Town Hall",
                                            "Parramatta, NSW",
                                            mode="transit",)
        #afficher le résultat
        print(directions_result)
    
    #def geolocalisation():
    #    city = 'london'
    #    api_url = 'https://api.api-ninjas.com/v1/geocoding?city='+city+''
    #    response = requests.get(api_url, headers={'X-Api-Key': '9ZhwyUW2uIaDzkXe5sdiYHPxJLGnahYLWNwA6UdX'})
    #    if response.status_code == requests.codes.ok:
    #        print(response.text)
    #    else:
    #        print("Error:", response.status_code, response.text)
    #    return response.text

    #def calculDistance():
    #    url = "https://api.myptv.com/routing/v1/routes?waypoints="+response.text["latitude"]+"&waypoints="+response.text["longitude"]+"&options[trafficMode]=AVERAGE"
    #    headers = {
    #        'apiKey': "RVVfNGUyN2U1NmU1M2U2NDM1NzhkODRjNGVmMjhmMmIxYzI6ZDNjMTc1ZmEtMTI0OS00OTk4LWJmN2QtMjk5M2I2YmU2ZGQy"
    #    }
    #    response = requests.request("GET", url, headers=headers)
    #    print(response.text.encode('utf8'))
    api()
    #geolocalisation()
    #calculDistance()