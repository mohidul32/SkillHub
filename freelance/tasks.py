# freelance/tasks.py
from celery import shared_task
from .models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@shared_task(name='freelance.generate_invoice')
def generate_invoice_task(order_pk):
    try:
        order = Order.objects.select_related('client', 'gig__freelancer').get(pk=order_pk)
    except Order.DoesNotExist:
        return f'order {order_pk} not found'
    # Very simple invoice generation example (string), in real world use PDF lib
    context = {'order': order}
    invoice_html = render_to_string('freelance/invoice.html', context)
    # send email to client
    email = EmailMessage(f'Invoice for order #{order.pk}', invoice_html, to=[order.client.email])
    email.content_subtype = 'html'
    email.send()
    return f'invoice sent for order {order.pk}'
