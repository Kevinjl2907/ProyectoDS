# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "Entra al siguiente link para poder reiniciar tu contraseña:" + \
    "\n{}?token={}".format("http://localhost:5173/#/auth/newpassword/", reset_password_token.key)
    send_mail(
        "Reinicio de contraseñar para {title}".format(title="plataforma institucional"), # titulo
        email_plaintext_message, # contenido del correo
        "platdigitalproject@gmail.com", # correo desde el que se manda
        [reset_password_token.user.email] # Correo al que se va a mandar
    )