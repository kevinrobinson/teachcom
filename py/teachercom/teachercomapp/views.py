# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from teachercomapp.models import Student, Message

def index(request):
    return render_to_response('index.html')

def send(request):
    if request.method == 'GET':
        students = Student.objects.order_by('first_name')
        messages = Message.objects.order_by('label')
        return render_to_response('send.html', {
            'students': students,
            'messages': messages
        })
