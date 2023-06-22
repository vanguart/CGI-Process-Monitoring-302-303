from django import template

register = template.Library()

@register.simple_tag
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_string = file.read()
        print(log_string)
    return log_string