from django.contrib.auth.models import User

import requests
import datetime

from drchrono_patients.settings import CLIENT_DATA
from models import Doctor, Patient, Problem, Medication, Allergy, Appointment


# Access drchrono API
def get_drchrono_user(request_params):
    """
    Get user data from drchrono api and update user and patients rows in db
    """
    access_token = exchange_token(request_params)
    current_doctor_data = get_doctor_data(access_token)
    user = save_user(current_doctor_data, access_token)
    get_patients(user, access_token)
    return user


def exchange_token(params):
    """
    Get access token from drchrono
    """
    content = {
        'code': params['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': CLIENT_DATA['redirect_url'],
        'client_id': CLIENT_DATA['client_id'],
        'client_secret': CLIENT_DATA['client_secret'],
    }

    response = requests.post('https://drchrono.com/o/token/', content)
    response.raise_for_status()
    data = response.json()
    return data['access_token']


def get_doctor_data(access_token):
    """
    Get doctor data for current drchrono user
    """
    header = {'Authorization': 'Bearer %s' % access_token}
    user_data = get_user_data(header)

    doctor_endpoint = 'doctors/{0}'.format(user_data['doctor'])
    data = get_drchrono_data(doctor_endpoint, header)
    data['username'] = user_data['username']
    return data


def get_user_data(header):
    """
    Get user data for current drchrono user
    """
    endpoint = 'users/current'
    current_doctor_data = get_drchrono_data(endpoint, header)
    return current_doctor_data


def save_user(doctor_data, access_token):
    user = User.objects.create_user(
        id=doctor_data['id'],
        username=doctor_data['username'],
        first_name=doctor_data['first_name'],
        last_name=doctor_data['last_name'],
        email=doctor_data['email']
    )

    doctor = Doctor(user=user, token=access_token)
    doctor.save()
    return user


def get_patients(user, access_token):
    endpoint = 'patients'
    patients = get_paginated_data(endpoint, access_token)

    for patient_data in patients:
        patient = save_patient(patient_data, user)
        get_patient_data(patient, access_token, user)


def save_patient(patient_data, user):
    patient = Patient(
        id=patient_data['id'],
        doctor=user,
        first_name=patient_data['first_name'],
        middle_name=patient_data['middle_name'],
        last_name=patient_data['last_name'],
        address=patient_data['address'],
        email=patient_data['email'],
        home_phone=patient_data['home_phone'],
        cell_phone=patient_data['cell_phone'],
        city=patient_data['city'],
        zip_code=patient_data['zip_code'],
        state=patient_data['state'],
        emergency_contact_name=patient_data['emergency_contact_name'],
        emergency_contact_phone=patient_data['emergency_contact_phone'],
        emergency_contact_relation=patient_data['emergency_contact_relation'],
        employer=patient_data['employer'],
        employer_city=patient_data['employer_city'],
        employer_state=patient_data['employer_state'],
        employer_address=patient_data['employer_address'],
        employer_zip_code=patient_data['employer_zip_code'],
        primary_care_physician=patient_data['primary_care_physician'],
        social_security_number=patient_data['social_security_number'],
        responsible_party_name=patient_data['responsible_party_name'],
        responsible_party_phone=patient_data['responsible_party_phone'],
        responsible_party_relation=patient_data['responsible_party_relation'],
        responsible_party_email=patient_data['responsible_party_email'],
    )

    patient.save()
    return patient


def get_patient_data(patient, access_token, user):
    problem_endpoint = 'problems?patient=%s' % patient.id
    problems = get_paginated_data(problem_endpoint, access_token)
    save_problems(problems, patient)

    med_endpoint = 'medications?patient=%s' % patient.id
    medications = get_paginated_data(med_endpoint, access_token)
    save_medications(medications, patient, user)

    allergies_endpoint = 'allergies?patient=%s' % patient.id
    allergies = get_paginated_data(allergies_endpoint, access_token)
    save_allergies(allergies, patient)

    # date = datetime.date.today().isoformat()
    # appointment_endpoint = 'appointments?date={0}&patient={1}'.format(
    #     date, patient.id
    # )
    # appointment = get_paginated_data(appointment_endpoint, access_token)
    # save_appointment(appointment, patient)

    # insurances = get_paginated_data('insurances', access_token)
    # save_insurances(insurances, patient)


def save_problems(problem_data, patient):
    for data in problem_data:
        problem = Problem(
            id=data['id'],
            patient=patient,
            date_changed=data['date_changed'],
            date_diagnosis=data['date_diagnosis'],
            date_onset=data['date_onset'],
            description=data['description'],
            name=data['name'],
            notes=data['notes'],
            status=data['status']
        )

        problem.save()


def save_medications(med_data, patient, user):
    for data in med_data:
        medication = Medication(
            id=data['id'],
            patient=patient,
            doctor=user,
            daw=data['daw'],
            name=data['name'],
            prn=data['prn'],
            date_prescribed=data['date_prescribed'],
            date_started_taking=data['date_started_taking'],
            date_stopped_taking=data['date_stopped_taking'],
            dispense_quantity=data['dispense_quantity'],
            dosage_quantity=data['dosage_quantity'],
            notes=data['notes'],
            frequency=data['frequency'],
            number_refills=data['number_refills'],
            order_status=data['order_status'],
            status=data['status']
        )

        medication.save()


# def save_appointment(appointment_data, patient):
#     for data in appointment_data:
#         appointment = Appointment(
#             patient=patient,
#             id=data['id'],
#             scheduled_time=data['scheduled_time'],
#             status=data['status'],
#         )
#         appointment.save()


# def save_insurances(insurance_data, patient):
#     for data in insurance_data['results']:
#         insurance = Insurance(
#             patient=patient,
#             payer_name=data['payer_name'],
#             state=data['state'],
#             ranks=data['status']
#         )
#         insurance.save()


def save_allergies(allergies_data, patient):
    for data in allergies_data:
        allergies = Allergy(
            patient=patient,
            id=data['id'],
            notes=data['notes'],
            reaction=data['reaction'],
            status=data['status'],
        )

        allergies.save()


def get_drchrono_data(endpoint, header):
    """
    Helper function to get data the from the drchrono api
    """
    response = requests.get(
        'https://drchrono.com/api/%s' % endpoint,
        headers=header
    )
    response.raise_for_status()
    data = response.json()
    return data


def get_paginated_data(endpoint, access_token):
    url = 'https://drchrono.com/api/%s' % endpoint
    header = {'Authorization': 'Bearer %s' % access_token}
    objects = []

    while url:
        response = requests.get(url, headers=header)
        data = response.json()
        for object_data in data['results']:
            objects.append(object_data)

        url = data['next']

    return objects
