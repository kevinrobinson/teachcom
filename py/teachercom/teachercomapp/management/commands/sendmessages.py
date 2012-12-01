from django.core.management.base import BaseCommand, CommandError
from django import template
from teachercomapp.models import Event, Student, Message
from twilio.rest import TwilioRestClient

class Command(BaseCommand):
    help = "Send messages queued to be sent in the (hopefully recent) past"
    
    def handle(self, *args, **kwargs):
        #conn = TwilioRestClient(<account>, <token>)
        for event in Event.objects.filter(result_of_message=4):
            if event.type_of_message == 1:
                # send sms
                t = template.Template(event.message.text)
                c = template.Context({'student': event.student})
                msg = t.render(c)

                #conn.sms.messages.create(
                #    to=event.student.phone_number,
                #    from_=<twilio phone number>,
                #    body=msg)
            elif event.type_of_message == 2:
                # send voice call
                #conn.calls.create(
                #    to=event.student.phone_number,
                #    from_=<twilio phone number>,
                #    url='<base url>/calls/%d' % (event.id))
            else:
                # send email, you know, if we get time
