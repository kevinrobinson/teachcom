from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Student(models.Model):
    student_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sms_notification_ind = models.BooleanField()
    call_notification_ind = models.BooleanField()
    email_notification_ind = models.BooleanField()
    phone_number = models.CharField(max_length=30)
    email= models.CharField(max_length=30)

class Message(models.Model):
    label = models.CharField(max_length=64)
    text = models.TextField()

class Event(models.Model):
    MESSAGE_TYPES =  (
        (1, 'sms'),
        (2, 'voice'),
        (3, 'email'),
        )
    RESULT_TYPES = (
        (0, 'success'),
        (1, 'busy'),
        (2, 'nopickup'),
        (3, 'failed'),
        )
    student = models.ForeignKey('Student')
    message = models.ForeignKey('Message')
    date_of_message = models.DateTimeField()
    time_of_message = models.DateTimeField()
    type_of_message = models.IntegerField(choices=MESSAGE_TYPES) 
    result_of_message = models.IntegerField(choices = RESULT_TYPES)

class Teacher(models.Model):
    user = models.OneToOneField(User)
    twilio_api_key=models.CharField(max_length=128)
    twilio_api_secret=models.CharField(max_length=128)

    def __str__(self):  
      return "%s's profile" % self.user  

def create_teacher(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Teacher.objects.get_or_create(user=instance)  

post_save.connect(create_teacher, sender=User)