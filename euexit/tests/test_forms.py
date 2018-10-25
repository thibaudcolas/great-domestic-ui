from unittest import mock

from directory_constants.constants import choices
import pytest

from euexit import forms, helpers


@pytest.mark.parametrize('form_class', (
    forms.InternationalContactForm, forms.DomesticContactForm
))
def test_contact_form_set_field_attributes(form_class):
    form_one = form_class(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
    )
    form_two = form_class(
        field_attributes={
            'first_name': {
                'label': 'Your given name',
            },
            'last_name': {
                'label': 'Your family name'
            }
        },
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
    )

    assert form_one.fields['first_name'].label is None
    assert form_one.fields['last_name'].label is None
    assert form_two.fields['first_name'].label == 'Your given name'
    assert form_two.fields['last_name'].label == 'Your family name'


def test_domestic_contact_form_serialize(captcha_stub):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'form_url': 'http://www.form.com',
        'ingress_url': 'http://www.ingress.com',
    }


def test_international_contact_form_serialize(captcha_stub):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': choices.COUNTRY_CHOICES[1][0],
            'city': 'London',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'form_url': 'http://www.form.com',
        'ingress_url': 'http://www.ingress.com',
    }


@mock.patch.object(forms.ZendeskActionMixin, 'action_class')
def test_international_contact_form_uses_eu_exit_client(
    mock_action, captcha_stub
):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': choices.COUNTRY_CHOICES[1][0],
            'city': 'London',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert form.is_valid()
    form.save(
        email_address='test@example.com',
        full_name='Jim Example',
        subject='Some subject',
        subdomain='some-subdomain',
    )

    assert mock_action.call_count == 1
    assert mock_action.call_args == mock.call(
        client=helpers.eu_exit_forms_api_client,
        subject='Some subject',
        full_name='Jim Example',
        email_address='test@example.com',
        subdomain='some-subdomain',
    )


@mock.patch.object(forms.ZendeskActionMixin, 'action_class')
def test_domestic_contact_form_uses_eu_exit_client(
    mock_action, captcha_stub
):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert form.is_valid()
    form.save(
        email_address='test@example.com',
        full_name='Jim Example',
        subject='Some subject',
        subdomain='some-subdomain',
    )

    assert mock_action.call_count == 1
    assert mock_action.call_args == mock.call(
        client=helpers.eu_exit_forms_api_client,
        subject='Some subject',
        full_name='Jim Example',
        email_address='test@example.com',
        subdomain='some-subdomain',
    )
