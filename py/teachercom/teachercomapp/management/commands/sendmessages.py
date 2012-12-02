from django.core.management.base import BaseCommand, CommandError
from django import template
from teachercomapp.models import Event, Student, Message
from twilio.rest import TwilioRestClient

class Command(BaseCommand):
    help = "Send messages queued to be sent in the (hopefully recent) past"
    
    def handle(self, *args, **kwargs):
        """ Note: this could be batched to thin out the
            number of requests """
        for event in Event.objects.filter(result_of_message=4):
            conn = TwilioRestClient(
                event.message.teacher.twilio_api_key,
                event.message.teacher.twilio_api_secret)
            if event.type_of_message == 1:
                # send sms
                t = template.Template(event.message.text)
                c = template.Context({'student': event.student})
                msg = t.render(c)
                
                try:
                    conn.sms.messages.create(
                        to = event.student.phone_number,
                        from_ = event.message.teacher.twilio_number,
                        body = msg[0:160])
                    event.result_of_message = 0
                except:
                    event.result_of_message = 3
                    
            elif event.type_of_message == 2:
                # send voice call
                conn.calls.create(
                    to = event.student.phone_number,
                    from_ = event.message.teacher.twilio_number,
                    url = 'http://www.teachercom.org/twilio_calls/%d' % (event.id))
            else:
                pass
                # send email, you know, if we get time
