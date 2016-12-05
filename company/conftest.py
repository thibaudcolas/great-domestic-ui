from copy import deepcopy
import http
from unittest.mock import patch

import requests
import pytest


@pytest.fixture
def list_public_profiles_data():
    return {
        'results': [
            {
                'sectors': ['SECTOR1', 'SECTOR2'],
                'number': '123456',
                'name': 'UK exporting co ltd.',
                'description': 'Exporters of UK wares.',
                'website': 'http://www.ukexportersnow.co.uk',
                'logo': 'www.ukexportersnow.co.uk/logo.png',
                'keywords': 'word1 word2',
                'date_of_creation': '2015-03-01',
                'employees': '1001-10000',
                'supplier_case_studies': [],
            }
        ],
        'count': 20
    }


@pytest.fixture
def supplier_case_study_data():
    return {
        'description': 'Damn great',
        'sector': 'SOFTWARE_AND_COMPUTER_SERVICES',
        'image_three': 'https://image_three.jpg',
        'website': 'http://www.google.com',
        'video_one': 'https://video_one.wav',
        'title': 'Two',
        'company': {
            'website': 'https://www.example.com',
            'employees': '1-10',
            'description': 'Good stuff.',
            'logo': 'https://logo.png',
            'date_of_creation': '2015-03-02',
            'name': 'EXAMPLE CORP',
            'supplier_case_studies': [],
            'keywords': 'Web development',
            'sectors': ['SOFTWARE_AND_COMPUTER_SERVICES'],
            'number': '09466004'
        },
        'image_one': 'https://image_one.jpg',
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'pk': 2,
        'year': '2000',
        'image_two': 'https://image_two.jpg'
    }


@pytest.fixture
def api_response_200():
    response = requests.Response()
    response.status_code = http.client.OK
    response.json = lambda: deepcopy({})
    return response


@pytest.fixture
def api_response_list_public_profile_200(
    api_response_200, list_public_profiles_data
):
    response = api_response_200
    response.json = lambda: deepcopy(list_public_profiles_data)
    return response


@pytest.fixture
def api_response_retrieve_supplier_case_study_200(supplier_case_study_data):
    response = api_response_200()
    response.json = lambda: deepcopy(supplier_case_study_data)
    return response


@pytest.fixture(autouse=True)
def retrieve_supplier_case_study_response(api_response_200):
    stub = patch(
        'api_client.api_client.company.retrieve_supplier_case_study',
        return_value=api_response_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def list_public_profiles(api_response_list_public_profile_200):
    stub = patch(
        'api_client.api_client.company.list_public_profiles',
        return_value=api_response_list_public_profile_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_supplier_case_study(
    api_response_retrieve_supplier_case_study_200
):
    stub = patch(
        'api_client.api_client.company.retrieve_supplier_case_study',
        return_value=api_response_retrieve_supplier_case_study_200,
    )
    stub.start()
    yield
    stub.stop()