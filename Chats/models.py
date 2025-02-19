from django.db import models


class Userss(models.Model):
    user_id  = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=12)
    active_chat = models.BooleanField(default=False)
    created_at = models.DateField()
    
class Conversations(models.Model):
    user1_id  = models.ForeignKey(Userss,on_delete=models.CASCADE,related_name='conversations_as_user1')
    user2_id  = models.ForeignKey(Userss,on_delete=models.CASCADE,related_name='conversations_as_user2')
    created_at = models.DateField()

class Messages(models.Model):
    conversation_id = models.ForeignKey(Conversations,on_delete=models.CASCADE,related_name='conversations_by_2user')
    sender_id = models.ForeignKey(Userss,on_delete=models.CASCADE,related_name='user_id_sender')
    content = models.TextField(max_length=400)
    created_at = models.DateField()
