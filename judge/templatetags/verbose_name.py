from django import template


register = template.Library()


@register.simple_tag
def model_name(model, num=1):
    try:
        return (model.model._meta.verbose_name if num == 1
                else model.model._meta.verbose_name_plural).capitalize()
    except AttributeError:
        return (model._meta.verbose_name if num == 1
                else model._meta.verbose_name_plural).capitalize()


@register.simple_tag
def field_name(instance, field):
    return instance._meta.get_field(field).verbose_name.capitalize()
