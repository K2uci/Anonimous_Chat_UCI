from django.http import JsonResponse , HttpRequest , HttpResponse
from django.db.models import Q
from .models import *
from datetime import datetime
import random

#POST
def register_user(request : HttpRequest , id : int , username : str ) -> HttpResponse:
    new_user = Userss()
    new_user.user_id  = id
    new_user.username = username
    new_user.created_at = datetime.now().strftime("%Y-%m-%d")
    if Userss.objects.filter(user_id=id).__len__() == 0:
        new_user.save()
    return HttpResponse()

#GET
def search_user_free(request : HttpRequest, id : int) -> JsonResponse:
        
    # Obtengo todos los usuarios libres
    users_ready = Userss.objects.exclude(
        Q(active_chat=True) | Q(user_id=id)
    )
    if users_ready.__len__() < 1:
        return JsonResponse({"user_id":None})
    
    # Seleccione un usuario rando y tambien el mio 
    user_selected = random.choice(users_ready)
    my_user = Userss.objects.get(user_id=id)
    
    # Elimino todas las conversaciones antiguas acerca de los usuarios
    old_conversation = Conversations.objects.filter(
        Q(user1_id=my_user.user_id) | Q(user2_id=my_user.user_id) 
    )
    if old_conversation.__len__() > 0:
        Userss.objects.filter(user_id=old_conversation[0].user1_id.user_id).update(active_chat=False)
        Userss.objects.filter(user_id=old_conversation[0].user2_id.user_id).update(active_chat=False)
        old_conversation.delete()
    
    # Creao una nueva conversacion
    new_conversation = Conversations()
    new_conversation.user1_id = my_user
    new_conversation.user2_id = user_selected
    new_conversation.created_at = datetime.now().strftime("%Y-%m-%d")
    new_conversation.save()
    
    # Actualizo el estado de ambos usuarios
    my_user.active_chat = True  
    my_user.save()
    user_selected.active_chat = True
    user_selected.save()

    return JsonResponse({"user_id":user_selected.user_id})

#GET
def take_breack(request : HttpRequest, id : int) -> JsonResponse:
    user_del = Userss.objects.filter(user_id=id)
    if user_del.__len__() == 1:
        user_del.delete()
    return JsonResponse()

#GET
def send_message(request : HttpRequest , id : int , sms : str) -> JsonResponse:
    
    # Obtengo mi usuario
    my_user = Userss.objects.get(user_id=id)
    # Creo un nuevo mensaje 
    new_sms = Messages()
    new_sms.conversation_id = Conversations.objects.get(
        Q(user1_id=my_user) | Q(user2_id=my_user)
    )
    new_sms.sender_id = my_user
    new_sms.content = sms
    new_sms.created_at = datetime.now().strftime("%Y-%m-%d")
    new_sms.save()
    
    # Obtengo el user_id del recividor
    conversation_instance = Conversations.objects.get(
        Q(user1_id=my_user) | Q(user2_id=my_user)
    )
    id_user_recived = conversation_instance.user1_id.user_id if my_user.user_id != conversation_instance.user1_id.user_id else conversation_instance.user2_id.user_id
    
    # Guardo la data para devolverla de mi usuario y el que recive
    data = {
        "id_user_send":my_user.user_id,
        "id_user_recived":id_user_recived
    }
    return JsonResponse(data)

#GET
def is_conversation(request : HttpRequest , id : int) -> JsonResponse:
    # Busco si el usuario esta en alguna conversacio
    is_in_conversation = Conversations.objects.filter(
        Q(user1_id=id) | Q(user2_id=id)
    )
    if is_in_conversation.__len__() == 1: 
        return JsonResponse({'is_active':True})
    else:
        return JsonResponse({'is_active':False})