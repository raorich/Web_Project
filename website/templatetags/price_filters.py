import locale
from django import template

register = template.Library()

@register.filter
def clean_price(value):
    try:
        value = float(value)
        # Establece el locale a español (puede requerir configuración del sistema)
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        return locale.format_string("%.2f", value, grouping=True)
    except (ValueError, TypeError, locale.Error):
        # Fallback si el locale no funciona
        if value.is_integer():
            return f"{int(value):,}".replace(",", ".")
        else:
            parts = f"{value:.2f}".split(".")
            return f"{int(parts[0]):,}".replace(",", ".") + "," + parts[1]
