from django import template

register = template.Library()


@register.filter
def checkuser(value):
    roles = value.roles 
    if roles == "modir" or roles =='dabir':
        return True
    else:
        return False