from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def getattribute(indexable, attr):
    return indexable.__getattribute__(attr)