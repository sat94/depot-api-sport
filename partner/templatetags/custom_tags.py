
from django import template


register = template.Library()

@register.filter
def phoneNumber(tel):
    phone = ' '.join([tel[i:i+2] for i in range(0, len(tel), 2)])
    return phone

 


