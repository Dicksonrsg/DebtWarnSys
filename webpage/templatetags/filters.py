from django import template
from django.template.defaultfilters import stringfilter

# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/

register = template.Library()

@register.filter(name="format_cpf")
@stringfilter
def format_cpf(cpf: str):
    try:
        if not cpf or not isinstance(cpf, str):
            return "000.000.000-00"

        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    except Exception as e:
        raise e
    
    
@register.filter(name="format_cnpj")
@stringfilter
def format_cnpj(cnpj: str):
    try:
        if not cnpj or not isinstance(cnpj, str):
            return "00.000.000/0000-00."

        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    except Exception as e:
        raise e 
