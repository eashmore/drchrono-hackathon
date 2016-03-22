import requests

from django.contrib.auth.models import User

from drchrono_patients.settings import CLIENT_DATA
from models import Patient, Problem, Medication, Insurance, Allergies

# Access drchrono API
def get_drchrono_user(request_params):
    """
    Get user data from drchrono api and update user and patients rows in db
    """
    access_token = exchange_token(request_params)
    current_doctor_data = get_doctor_data(access_token)
    user = save_user(current_doctor_data)
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


def save_user(doctor_data):
    user = User.objects.create_user(
        id=doctor_data['id'],
        username=doctor_data['username'],
        first_name=doctor_data['first_name'],
        last_name=doctor_data['last_name'],
        email=doctor_data['email']
    )

    return user


def get_patients(user, access_token):
    """
    Find the current user's patients and insert/update patient's row in db
    """
    patients_url = 'https://drchrono.com/api/patients'
    header = {'Authorization': 'Bearer %s' % access_token}
    while patients_url:
        response = requests.get(patients_url, headers=header)
        data = response.json()
        for patient_data in data['results']:
            patient = save_patient(patient_data, user)
            get_patient_data(patient, header)

        patients_url = data['next']


def save_patient(patient_data, user):
    patient_attrs = Patient.column_list()
    kwargs = {}
    for attr in patient_attrs:
        kwargs[attr] = patient_data[attr]

    kwargs['doctor'] = user
    patient = Patient(**kwargs)

    patient.save()
    return patient

def get_patient_data(patient, header):
    endpoint = 'problems/?patient=%s' % patient.id
    problems = get_drchrono_data(endpoint, header)
    import pdb; pdb.set_trace()

    save_problems(problems, patient)

    medications = get_drchrono_data('medications', header)
    save_medications(medications, patient)

    # insurances = get_drchrono_data('insurances', header)
    # save_insurances(insurances, patient)

    allergies = get_drchrono_data('allergies', header)
    save_allergies(allergies, patient)


def save_problems(problem_data, patient):
    for data in problem_data['results']:
        problem = Problem(
            patient = patient,
            date_changed = data['date_changed'],
            date_diagnosis = data['date_diagnosis'],
            date_onset = data['date_onset'],
            description = data['description'],
            name = data['name'],
            notes = data['notes'],
            status = data['status']
        )
        problem.save()


def save_medications(med_data, patient):
    for data in med_data['results']:
        medication = Medication(
            patient = patient,
            daw = data['daw'],
            name = data['name'],
            prn = data['prn'],
            date_prescribed = data['date_prescribed'],
            date_started_taking = data['date_started_taking'],
            date_stopped_taking = data['date_stopped_taking'],
            dispense_quantity = data['dispense_quantity'],
            dosage_quantity = data['dosage_quantity'],
            notes = data['notes'],
            frequency = data['frequency'],
            number_refills = data['number_refills'],
            order_status = data['order_status'],
            status = data['status']
        )
        medication.save()


# def save_insurances(insurance_data, patient):
#     for data in insurance_data['results']:
#         insurance = Insurance(
#             patient = patient,
#             payer_name = data['payer_name'],
#             state = data['state'],
#             ranks = data['status']
#         )
#         insurance.save()


def save_allergies(allergies_data, patient):
    for data in allergies_data['results']:
        allergies = Allergies(
            description = data['description'],
            notes = data['notes'],
            reaction = data['reaction'],
            status = data['status']
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
