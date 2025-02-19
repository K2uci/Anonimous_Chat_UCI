from django.urls import path
from .views import * 

urlpatterns = [
    path('register/<int:id>/<str:username>', register_user),
    path('search/<int:id>', search_user_free),
    path('breack/<int:id>', take_breack),
    path('sendsms/<int:id>/<str:sms>', send_message),
    path('isactive/<int:id>',is_conversation)
]
