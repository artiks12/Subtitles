import requests
import sys
from tilde.ids import client_id, system_id
# client_id=sys.argv[1]
# system_id=sys.argv[2]
# text=sys.argv[3]
def translate(text):
    
    response = requests.post('https://www.letsmt.eu/ws/service.svc/json/TranslateEx',
                            headers={'Content-Type': 'application/json',
                                    'client-id': client_id},
                            json={'appID': 'TechChillDemo',
                                'systemID': system_id,
                                'text': text,
                                'options': 'alignment,markSentences,tagged'})
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e.response.status_code)
        print(e.response.content)
    return response.json()
