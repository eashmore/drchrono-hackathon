from django.core.mail import send_mail
from django.forms.models import model_to_dict

import datetime

from drchrono_patients.settings import EMAIL_HOST_USER


def date_to_str(date):
    if date:
        return date.isoformat()

    return None


def num_to_str(field):
    if field:
        return field

    return ''


def str_to_date(date_str):
    if date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')

    return None


# send message to doctor
def send_message(email, message, patient):
    subject = 'A message from {0} {1}'.format(
        patient.first_name, patient.last_name
    )
    send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)


def send_update_message(email, instance, old_instance):
    patient = instance.patient
    subject = '{0} {1} had updated a new {2}'
    subject = subject.format(
        patient.first_name, patient.last_name, type(instance).__name__
    )
    message = ('The following updates have been applied to {0} id: {1} '
               'by {2} {3}:\n\n')
    message = message.format(
        type(instance).__name__,
        instance.id,
        patient.first_name,
        patient.last_name
    )
    message += stringify_instance(instance, old_instance)
    send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)


def send_create_mail(email, instance):
    patient = instance.patient
    subject = '{0} {1} has added a new {2}'
    subject = subject.format(
        patient.first_name, patient.last_name, type(instance).__name__
    )
    message = 'The following {0} has been added by {1} {2}:\n\n'.format(
        type(instance).__name__, patient.first_name, patient.last_name
    )
    message += stringify_instance(instance)

    send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)


def stringify_instance(instance, old_instance=False):
    if old_instance:
        instance_dict = model_to_dict(instance)
        attr_dict = {}
        for key in instance_dict:
            if instance_dict[key] != old_instance[key]:
                attr_dict[key] = instance_dict[key]
    else:
        attr_dict = model_to_dict(instance)

    return build_message(attr_dict)


def build_message(attr_dict):
    message = ''
    for key in attr_dict:
        if key != 'id':
            message += "{0}: {1}\n".format(key, attr_dict[key])

    return message
