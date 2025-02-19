import requests
from Config.Config import URL

# Funcion para registrar 
def register(id : int , username : str):
    requests.get(f'{URL}/register/{id}/{username}')

# Funcion para buscar usuarios free devuelve si hay o no
def search_by_id(id : int) -> bool:
    answer = requests.get(f'{URL}/search/{id}')
    return True if  not answer.json()['user_id'] else False

# Funcion para mandar mensage
def send_message_own(id : int , sms : str) -> int | None:
    if aux_in_conversation(id):
        return requests.get(f'{URL}/sendsms/{id}/{sms}').json()['id_user_recived']
    else:
        return None

def aux_in_conversation(id : int) -> bool:
    return requests.get(f'{URL}/isactive/{id}').json()['is_active']

# Funcion para eliminar usuario
def take_breack(id : int):
    requests.get(f'{URL}/breack/{id}')


