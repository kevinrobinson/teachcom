# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from teachercomapp.models import Student, Message, Event
import datetime

@cache_page(1)
def index(request):
    return render_to_response('index.html')

def send(request):
    if request.method == 'GET':
        data = {
            'students': Student.objects.order_by('first_name'),
            'messages': Message.objects.order_by('label')
        }

        data.update(csrf(request))
        return render_to_response('send.html', data)
    else:
        message = Message.objects.get(pk=request.POST['message'])
        for student_id in request.POST['students']:
            student = Student.objects.get(pk=student_id)
            if student.sms_notification_ind:
                send_message(student, message, 1)
            if student.call_notification_ind:
                send_message(student, message, 2)
            if student.email_notification_ind:
                send_message(student, message, 3)
        return render_to_response('sent.html')

def send_message(student, message, message_type):
    event = Event(student=student, message=message,
        date_of_message=datetime.datetime.now(),
        type_of_message=message_type,
        result_of_message=4)
    event.save()
