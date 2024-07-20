import requests
from django.core.cache import cache
from createTeam.models import Team

def get_whatsapp_credentials(team_id):
    credentials = cache.get(f'whatsapp_credentials_{team_id}')
    if not credentials:
        team = Team.objects.get(id=team_id)
        access_token = team.accessToken

        # Get WhatsApp Business ID
        url = f"https://graph.facebook.com/v20.0/debug_token?input_token={access_token}"

        payload = {}
        headers = {
        'Authorization': f'Bearer {access_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        business_response = response.json()
        whatsapp_business_id = business_response['data']['granular_scopes'][0]['target_ids'][0]

        phone_number_response = requests.get(
            f'https://graph.facebook.com/v20.0/{whatsapp_business_id}/phone_numbers',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        phone_number_data = phone_number_response.json()
        phone_number_id = phone_number_data['data'][0]['id']

        credentials = {
            'auth_token': access_token,
            'whatsapp_business_id': whatsapp_business_id,
            'phone_number_id': phone_number_id,
        }
        cache.set(f'whatsapp_credentials_{team_id}', credentials, timeout=3600)
    return credentials