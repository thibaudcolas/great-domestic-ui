from directory_constants.constants import cms

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.mixins import GetCMSPageMixin
from contact import constants, forms


def build_export_opportunites_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-export-opportunities-guidance', kwargs={'slug': step_name}
    )


def build_great_account_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-great-account-guidance', kwargs={'slug': step_name}
    )


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['CONTACT_US_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class RoutingFormView(FeatureFlagMixin, NamedUrlSessionWizardView):

    # given the current step, based on selected  option, where to redirect.
    redirect_mapping = {
        constants.DOMESTIC: {
            constants.TRADE_OFFICE: settings.FIND_TRADE_OFFICE_URL,
            constants.EXPORT_ADVICE: reverse_lazy('contact-us-export-advice'),
            constants.FINANCE: reverse_lazy(
                'uk-export-finance-lead-generation-form',
                kwargs={'step': 'contact'}
            ),
            constants.INVESTING: (
                reverse_lazy('eu-exit-invest-overseas-contact-form')
            ),
            constants.EUEXIT: reverse_lazy('eu-exit-domestic-contact-form'),
            constants.EVENTS: reverse_lazy('contact-us-events-form'),
            constants.DSO: reverse_lazy('contact-us-domestic'),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.INTERNATIONAL: {
            constants.INVESTING: settings.INVEST_CONTACT_URL,
            constants.BUYING: reverse_lazy('contact-us-find-uk-companies'),
            constants.EUEXIT: reverse_lazy(
                'eu-exit-international-contact-form'
            ),
            constants.OTHER: reverse_lazy('contact-us-international'),
        },
        constants.EXPORT_OPPORTUNITIES: {
            constants.NO_RESPONSE: reverse_lazy('contact-us-domestic'),
            constants.ALERTS: build_export_opportunites_guidance_url(
                cms.EXPORT_READINESS_HELP_EXOPP_ALERTS_IRRELEVANT_SLUG
            ),
            constants.MORE_DETAILS: reverse_lazy('contact-us-domestic'),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_SERVICES: {
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_ACCOUNT: {
            constants.NO_VERIFICATION_EMAIL: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_MISSING_VERIFY_EMAIL_SLUG
            ),
            constants.PASSWORD_RESET: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_PASSWORD_RESET_SLUG
            ),
            constants.COMPANIES_HOUSE_LOGIN: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_COMPANIES_HOUSE_LOGIN_SLUG
            ),
            constants.VERIFICATION_CODE: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_ENTER_SLUG,
            ),
            constants.NO_VERIFICATION_LETTER: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_LETTER_SLUG
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        }
    }

    form_list = (
        (constants.LOCATION, forms.LocationRoutingForm),
        (constants.DOMESTIC, forms.DomesticRoutingForm),
        (constants.GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (constants.GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (constants.EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesRoutingForm),
        (constants.INTERNATIONAL, forms.InternationalRoutingForm),
        ('NO-OPERATION', forms.NoOpForm),  # should never be reached
    )
    templates = {
        constants.LOCATION: 'contact/routing/step-location.html',
        constants.DOMESTIC: 'contact/routing/step-domestic.html',
        constants.GREAT_SERVICES: 'contact/routing/step-great-services.html',
        constants.GREAT_ACCOUNT: 'contact/routing/step-great-account.html',
        constants.EXPORT_OPPORTUNITIES: (
            'contact/routing/step-export-opportunities-service.html'
        ),
        constants.INTERNATIONAL: 'contact/routing/step-international.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_redirect_url(self, choice):
        if self.steps.current in self.redirect_mapping:
            mapping = self.redirect_mapping[self.steps.current]
            return mapping.get(choice)

    def render_next_step(self, form):
        choice = form.cleaned_data['choice']
        redirect_url = self.get_redirect_url(choice)
        if redirect_url:
            return redirect(redirect_url)
        return self.render_goto_step(choice)


class FeedbackFormView(FeatureFlagMixin, FormView):
    form_class = forms.FeedbackForm
    template_name = 'contact/comment-contact.html'

    success_url = reverse_lazy('contact-us-domestic-success')

    def form_valid(self, form):
        response = form.save(
            email_address=form.cleaned_data['email'],
            full_name=form.cleaned_data['name'],
            subject=settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT,
        )
        response.raise_for_status()
        return super().form_valid(form)


class BuyingFromUKCompaniesFormView(FeatureFlagMixin, FormView):
    form_class = forms.BuyingFromUKContactForm
    template_name = 'contact/buying/step.html'


class InternationalFormView(FeatureFlagMixin, FormView):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'


class SendNotifyMessagesMixin:

    def send_agent_message(self, form):
        response = form.save(
            template_id=self.notify_template_id_agent,
            email_address=self.notify_email_address_agent,
        )
        response.raise_for_status()

    def send_user_message(self, form):
        response = form.save(
            template_id=self.notify_template_id_user,
            email_address=form.cleaned_data['email'],
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_message(form)
        self.send_user_message(form)
        return super().form_valid(form)


class DomesticFormView(FeatureFlagMixin, SendNotifyMessagesMixin, FormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')

    notify_template_id_agent = settings.CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID


class EventsFormView(FeatureFlagMixin, SendNotifyMessagesMixin, FormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')

    notify_template_id_agent = settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID


class DefenceAndSecurityOrganisationFormView(
    FeatureFlagMixin, SendNotifyMessagesMixin, FormView
):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')

    notify_template_id_agent = settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID


class InvestOverseasFormView(
    FeatureFlagMixin, SendNotifyMessagesMixin, FormView
):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')

    notify_template_id_agent = settings.CONTACT_INVEST_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_INVEST_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_INVEST_USER_NOTIFY_TEMPLATE_ID


class DomesticFormSuccessView(FeatureFlagMixin, GetCMSPageMixin, TemplateView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_SLUG


class GuidanceView(FeatureFlagMixin, GetCMSPageMixin, TemplateView):
    template_name = 'contact/guidance.html'

    @property
    def slug(self):
        return self.kwargs['slug']