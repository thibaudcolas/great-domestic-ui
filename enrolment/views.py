import logging

from formtools.wizard.views import NamedUrlSessionWizardView

from django.shortcuts import Http404, redirect
from django.template.response import TemplateResponse
from django.utils.cache import patch_response_headers
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from enrolment import forms, helpers
from sso.utils import SSOLoginRequiredMixin


logger = logging.getLogger(__name__)


class CacheMixin:

    def render_to_response(self, context, **response_kwargs):
        # Get response from parent TemplateView class
        response = super().render_to_response(
            context, **response_kwargs
        )

        # Add Cache-Control and Expires headers
        patch_response_headers(response, cache_timeout=60 * 30)

        # Return response
        return response


class HandleBuyerFormSubmitMixin:
    success_template = 'landing-page-international-success.html'
    form_class = forms.InternationalBuyerForm

    def form_valid(self, form):
        data = forms.serialize_international_buyer_forms(form.cleaned_data)
        api_client.buyer.send_form(data)
        return TemplateResponse(self.request, self.success_template)


class CachableTemplateView(CacheMixin, TemplateView):
    pass


class DomesticLandingView(TemplateView):
    template_name = 'landing-page.html'


class InternationalLandingView(HandleBuyerFormSubmitMixin, FormView):
    template_name = 'landing-page-international.html'


class InternationalLandingSectorListView(HandleBuyerFormSubmitMixin, FormView):
    template_name = 'landing-page-international-sector-list.html'


class InternationalLandingSectorDetailView(HandleBuyerFormSubmitMixin,
                                           FormView):
    templates = {
        'health': 'landing-page-international-sector-detail-health.html',
        'tech': 'landing-page-international-sector-detail-tech.html',
        'creative': 'landing-page-international-sector-detail-creative.html',
        'food-and-drink': 'landing-page-international-sector-detail-food.html',
    }

    contexts = {
        'health': {
            'case_study': {
                'image_url': '/static/images/health-case-study-hero-image.png',
                'title': 'Touch Bionics',
                'synopsis': (
                    'Touch Bionics has transformed thousands of lives in '
                    'dozens of countries worldwide through its world-leading '
                    'prosthetic technologies. We have a range of myoelectric '
                    'prosthetic hand and prosthetic finger solutions to help '
                    'people increase their independence and confidence.'
                ),
                'url': '#',
                'testimonial': (
                    'Lorem ipsum dolor sit amet consectetur adipiscing elit '
                    'sed do eiusmod tempor incididunt ut labore et dolore '
                    'magna aliqua. Ut enim ad minim'
                ),
                'testimonial_name': 'Firstname Surname',
                'testimonial_company': 'Company name',
                'company_name': 'Touch Bionics',
                'sector_url': '#',
                'sector_name': 'Technology',
                'keywords': (
                    'Robotics, Limb Loss, Prosthetics, Healthcare, '
                    'Technology, Bionics'
                ),
            },
            'companies': [
                {
                    'image_url': '/static/images/sector-image.png',
                    'name': 'Cool Corp',
                    'descrition': (
                        'Build labs, factories and clinical facilities with '
                        'UK infrastructure know-how lorem ipsum dolor sit'
                    ),
                    'public_profile_url': '#',
                },
                {
                    'image_url': '/static/images/sector-image.png',
                    'name': 'Cool Corp',
                    'descrition': (
                        'Training and education in the UK lorem ipsum dolor '
                        'sit'
                    ),
                    'public_profile_url': '#',
                },
            ]
        }
    }

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['slug'] not in self.templates:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [self.templates[self.kwargs['slug']]]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(self.contexts[self.kwargs['slug']])
        return context


class EnrolmentInstructionsView(TemplateView):
    template_name = 'enrolment-instructions.html'

    def dispatch(self, request, *args, **kwargs):
        sso_user = request.sso_user
        if sso_user and helpers.has_company(sso_user.id):
            return redirect('company-detail')
        return super().dispatch(request, *args, **kwargs)


class EnrolmentView(SSOLoginRequiredMixin, NamedUrlSessionWizardView):

    COMPANY = 'company-number'
    NAME = 'company-name'
    STATUS = 'exports'

    success_template = 'registered.html'
    failure_template = 'enrolment-error.html'
    form_list = (
        (COMPANY, forms.CompanyForm),
        (NAME, forms.CompanyNameForm),
        (STATUS, forms.CompanyExportStatusForm),
    )
    templates = {
        COMPANY: 'company-form.html',
        NAME: 'company-form-name.html',
        STATUS: 'export-status-form.html',
    }

    def dispatch(self, request, *args, **kwargs):
        if request.sso_user is None:
            return self.handle_no_permission()
        elif helpers.has_company(request.sso_user.id):
            return redirect('company-detail')
        else:
            return super(EnrolmentView, self).dispatch(
                request, *args, **kwargs
            )

    def get_form_kwargs(self, step):
        if step == self.COMPANY:
            return {
                'session': self.request.session,
            }
        return {}

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_form_initial(self, step):
        if step == self.NAME:
            name = helpers.get_company_name_from_session(self.request.session)
            return forms.get_company_name_form_initial_data(name=name)

    def serialize_form_data(self):
        data = forms.serialize_enrolment_forms(self.get_all_cleaned_data())
        date_of_creation = helpers.get_company_date_of_creation_from_session(
            self.request.session
        )
        data['sso_id'] = self.request.sso_user.id
        data['company_email'] = self.request.sso_user.email
        data['date_of_creation'] = date_of_creation
        return data

    def done(self, *args, **kwags):
        data = self.serialize_form_data()
        response = api_client.registration.send_form(data)
        if response.ok:
            template = self.success_template
        else:
            template = self.failure_template
        return TemplateResponse(self.request, template)
