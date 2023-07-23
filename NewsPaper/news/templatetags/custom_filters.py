from django import template

register = template.Library()


@register.filter()
def censor(target):
    return target.replace('едиска', '******')