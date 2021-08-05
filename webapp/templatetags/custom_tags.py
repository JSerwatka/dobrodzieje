from django import template


register = template.Library()

@register.simple_tag
def get_arrayfield_display(obj, *, arrayfield):
    '''
    Like get_foo_display but for ArrayField.
    
    For given model object with ArrayField with ChoiceField finds corresponding choice labels.
    '''

    # Get obj's class -> lookfor arrayfield -> its charfield -> its choices
    choices_of_given_field = obj.__class__._meta.get_field(arrayfield).base_field.choices
    
    objects_arrayfield_data = getattr(obj, arrayfield)

    return [dict(choices_of_given_field)[key] for key in objects_arrayfield_data]