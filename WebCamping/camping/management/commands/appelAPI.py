from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def geolocalisation():
        city = 'london'
        api_url = 'https://api.api-ninjas.com/v1/geocoding?city=london'
        response = requests.get(api_url, headers={'X-Api-Key': '9ZhwyUW2uIaDzkXe5sdiYHPxJLGnahYLWNwA6UdX'})
        if response.status_code == requests.codes.ok:
            print(response.text)
        else:
            print("Error:", response.status_code, response.text)
    geolocalisation()