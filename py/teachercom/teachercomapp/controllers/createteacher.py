from teachercomapp.forms import UserRegistrationForm
from django.contrib.auth.models import User

from teachercomapp.models import Teacher

from registration.signals import user_registered

# create teacher takes as kwargs a form input from the registration form, including user info and the twilio info
def create_teacher(sender, **kwargs):
    request = kwargs['request'].POST  
    form=UserRegistrationForm(request)
    extended_user = Teacher()
    extended_user.user = User.objects.get(username=request['username'])
    extended_user.twilio_api_key = request['twilio_api_key']
    extended_user.twilio_api_secret = request['twilio_api_secret']
    extended_user.twilio_number=request['twilio_number']
    extended_user.save()
    print "teacher created"

user_registered.connect(create_teacher)