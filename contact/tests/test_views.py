from unittest import mock

from directory_constants.constants import cms
import pytest

from django import forms
from django.conf import settings
from django.urls import reverse

from contact import constants, views


def build_wizard_url(step):
    return reverse('triage-wizard', kwargs={'step': step})


class ChoiceForm(forms.Form):
    choice = forms.CharField()


@pytest.fixture
def domestic_form_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'organisation_name': 'Example corp',
        'postcode': '**** ***',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.mark.parametrize('current_step,choice,expected_url', (
    # location step routing
    (
        constants.LOCATION,
        constants.DOMESTIC,
        build_wizard_url(constants.DOMESTIC),
    ),
    (
        constants.LOCATION,
        constants.INTERNATIONAL,
        build_wizard_url(constants.INTERNATIONAL),
    ),
    # domestic step routing
    (
        constants.DOMESTIC,
        constants.TRADE_OFFICE,
        settings.FIND_TRADE_OFFICE_URL,
    ),
    (
        constants.DOMESTIC,
        constants.EXPORT_ADVICE,
        reverse('contact-us-export-advice'),
    ),
    (
        constants.DOMESTIC,
        constants.FINANCE,
        reverse(
            'uk-export-finance-lead-generation-form',
            kwargs={'step': 'contact'},
        )
    ),
    (
        constants.DOMESTIC,
        constants.INVESTING,
        reverse('eu-exit-invest-overseas-contact-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EUEXIT,
        reverse('eu-exit-domestic-contact-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EVENTS,
        reverse('contact-us-events-form'),
    ),
    (
        constants.DOMESTIC,
        constants.DSO,
        reverse('contact-us-domestic')
    ),
    (
        constants.DOMESTIC,
        constants.OTHER,
        reverse('contact-us-domestic')
    ),
    # great services guidance routing
    (
        constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES,
        build_wizard_url(constants.EXPORT_OPPORTUNITIES),
    ),
    (
        constants.GREAT_SERVICES,
        constants.GREAT_ACCOUNT,
        build_wizard_url(constants.GREAT_ACCOUNT),
    ),
    (
        constants.GREAT_SERVICES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_EMAIL,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_MISSING_VERIFY_EMAIL_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.PASSWORD_RESET,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_PASSWORD_RESET_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.COMPANIES_HOUSE_LOGIN,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_COMPANIES_HOUSE_LOGIN_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.VERIFICATION_CODE,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_ENTER_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_LETTER,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_LETTER_SLUG
        )
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # Export opportunities guidance routing
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.NO_RESPONSE,
        reverse('contact-us-domestic'),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.ALERTS,
        views.build_export_opportunites_guidance_url(
            cms.EXPORT_READINESS_HELP_EXOPP_ALERTS_IRRELEVANT_SLUG
        ),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.MORE_DETAILS,
        reverse('contact-us-domestic'),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # international routing
    (
        constants.INTERNATIONAL,
        constants.INVESTING,
        settings.INVEST_CONTACT_URL,
    ),
    (
        constants.INTERNATIONAL,
        constants.BUYING,
        reverse('contact-us-find-uk-companies'),
    ),
    (
        constants.INTERNATIONAL,
        constants.EUEXIT,
        reverse('eu-exit-international-contact-form'),
    ),
    (
        constants.INTERNATIONAL,
        constants.OTHER,
        reverse('contact-us-international'),
    ),
))
def test_render_next_step(current_step, choice, expected_url):
    form = ChoiceForm(data={'choice': choice})

    view = views.RoutingFormView()
    view.steps = mock.Mock(current=current_step)
    view.storage = mock.Mock()
    view.url_name = 'triage-wizard'

    assert form.is_valid()
    assert view.render_next_step(form).url == expected_url


@mock.patch.object(views.FeedbackFormView.form_class, 'save')
def test_feedback_form_submit_success(mock_save, client, captcha_stub):
    url = reverse('contact-us-feedback')
    data = {
        'name': 'Test Example',
        'email': 'test@example.com',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('contact-us-domestic-success')

    assert mock_save.call_count == 1
    assert mock_save.call_args == mock.call(
        email_address=data['email'],
        full_name=data['name'],
        subject=settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT,
    )


@pytest.mark.parametrize('url,agent_template,user_template,agent_email', (
    (
        reverse('contact-us-events-form'),
        settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-dso-form'),
        settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-domestic'),
        settings.CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('eu-exit-invest-overseas-contact-form'),
        settings.CONTACT_INVEST_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_INVEST_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_INVEST_AGENT_EMAIL_ADDRESS,
    )

))
@mock.patch.object(views.EventsFormView.form_class, 'save')
def test_generic_domestic_form_submit_success(
    mock_save, client, captcha_stub, settings, domestic_form_data,
    url, agent_template, user_template, agent_email
):
    response = client.post(url, domestic_form_data)

    assert response.status_code == 302
    assert response.url == reverse('contact-us-domestic-success')

    assert mock_save.call_count == 2
    assert mock_save.call_args_list == [
        mock.call(
            template_id=agent_template,
            email_address=agent_email,
        ),
        mock.call(
            template_id=user_template,
            email_address=domestic_form_data['email'],
        )
    ]