from django.core.mail import send_mail
from django.conf import settings

def enviar_email_interesse(interesse):
    assunto = f"Novo interesse no software {interesse.software.nome}"

    mensagem= f"""
Olá {interesse.software.vendedor.username},

Você recebeu um novo interesse no software: {interesse.software.nome}

Mensagem:
{interesse.mensagem}

Acesse o painel para responder.
"""

    send_mail(
        assunto,
        mensagem,
        settings.EMAIL_HOST_USER,
        [interesse.software.vendedor.email],
        fail_silently=False,
    )

def enviar_email_resposta(interesse):
    assunto = f"Seu interesse em {interesse.software.nome} foi respondido"

    mensagem= f"""
Olá {interesse.usuario.username},

O vendedor respondeu seu interesse no software {interesse.software.nome}

Resposta:
{interesse.resposta_vendedor}

Acesse sua área logada para visualizar
"""

    send_mail(
        assunto,
        mensagem,
        settings.EMAIL_HOST_USER,
        [interesse.usuario.email],
        fail_silently=False,
    )