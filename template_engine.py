def render_template(template, **kwargs):
    result = template
    for key, value in kwargs.items():
        placeholder = '{{ ' + key + ' }}'

        # Заменяем место-для-подстановки в шаблоне на значение
        result = result.replace(placeholder, str(value))

    return result
