import requests
import sys
client_id=sys.argv[1]
response = requests.get('https://www.letsmt.eu/ws/service.svc/json/GetSystemList',
                         headers={'Content-Type': 'application/json',
                                  'client-id': client_id},
                         json={'appID': 'TechChillDemo',
                               'uiLanguageID': 'en',
                               'options': ''})
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(e.response.status_code)
    print(e.response.content)
systems = response.json()['System']
for system in systems:
    print("System for {}-{}: '{}'".format(system['SourceLanguage']['Code'],
                                          system['TargetLanguage']['Code'],
                                          system['Title']['Text']))
    print("ID: {}".format(system['ID']))
    print()

