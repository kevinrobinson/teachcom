from django.db import models

# Create your models here.
class Students(models.Model):
	student_id = models.BigIntegerField().unique 
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	sms_notification_ind = models.BooleanField()
	call_notification_ind = models.BooleanField()
	email_notification_ind = models.BooleanField()
	phone_number = models.CharField(max_length=30)
	email= models.CharField(max_length=30)

class Messages(models.Model):
	message_id = models.BigIntegerField()
	text = models.TextField()

class Events(models.Model):
	event_id = models.BigIntegerField()
	student_id = models.ForeignKey('Students')
	message_id = models.ForeignKey('Messages')
	date_of_message = models.DateTimeField()
	time_of_message = models.DateTimeField()
	type_of_message = models.IntegerField() #Create a dict for this
	result_of_message = models.IntegerField() #and this