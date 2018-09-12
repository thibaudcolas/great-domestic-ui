import directory_components.views

from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

import article.views
import casestudy.views
import contact.views
import core.views
import healthcheck.views
import triage.views
import finance.views
import invest.views
from conf.url_redirects import redirects


sitemaps = {
    'static': core.views.StaticViewSitemap,
    'contact': core.views.ContactUsSitemap,
}


urlpatterns = [
    url(
        r"^sitemap\.xml$", sitemap, {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        directory_components.views.RobotsView.as_view(),
        name='robots'
    ),
    url(
        r"^$",
        core.views.LandingPageView.as_view(),
        name='landing-page',
    ),
    url(
        r"^international/$",
        core.views.InternationalLandingPageView.as_view(),
        name='landing-page-international'
    ),
    url(
        r"^not-found/$",
        TemplateView.as_view(template_name='404.html'),
        name='not-found'
    ),
    url(
        r"^performance-dashboard/$",
        core.views.PerformanceDashboardGreatView.as_view(),
        name='performance-dashboard'
    ),
    url(
        r"^performance-dashboard/export-opportunities/$",
        core.views.PerformanceDashboardExportOpportunitiesView.as_view(),
        name='performance-dashboard-export-opportunities'
    ),
    url(
        r"^performance-dashboard/selling-online-overseas/$",
        core.views.PerformanceDashboardSellingOnlineOverseasView.as_view(),
        name='performance-dashboard-selling-online-overseas'
    ),
    url(
        r"^performance-dashboard/trade-profiles/$",
        core.views.PerformanceDashboardTradeProfilesView.as_view(),
        name='performance-dashboard-trade-profiles'
    ),
    url(
        r"^performance-dashboard/invest/$",
        core.views.PerformanceDashboardInvestView.as_view(),
        name='performance-dashboard-invest'
    ),
    url(
        r"^performance-dashboard/guidance-notes/$",
        core.views.PerformanceDashboardNotesView.as_view(),
        name='performance-dashboard-notes'
    ),
    url(
        r"^about/$",
        core.views.AboutView.as_view(),
        name='about'
    ),
    url(
        r"^privacy-and-cookies/$",
        core.views.PrivacyCookiesDomesticCMS.as_view(),
        name='privacy-and-cookies'
    ),
    url(
        r"^terms-and-conditions/$",
        core.views.TermsConditionsDomesticCMS.as_view(),
        name='terms-and-conditions'
    ),
    url(
        r"^international/privacy-and-cookies/$",
        core.views.PrivacyCookiesInternationalCMS.as_view(),
        name='privacy-and-cookies-international'
    ),
    url(
        r"^international/terms-and-conditions/$",
        core.views.TermsConditionsInternationalCMS.as_view(),
        name='terms-and-conditions-international'
    ),
    url(
        r"^export-opportunities/$",
        core.views.InterstitialPageExoppsView.as_view(),
        name='export-opportunities',
    ),
    url(
        r"^new/$",
        article.views.PersonaNewArticleListView.as_view(),
        name='article-list-persona-new',
    ),
    url(
        r"^occasional/$",
        article.views.PersonaOccasionalArticleListView.as_view(),
        name='article-list-persona-occasional',
    ),
    url(
        r"^regular/$",
        article.views.PersonaRegularArticleListView.as_view(),
        name='article-list-persona-regular',
    ),
    url(
        r"^market-research/$",
        article.views.MarketResearchArticleListView.as_view(),
        name='article-list-market-research',
    ),
    url(
        r"^customer-insight/$",
        article.views.CustomerInsightArticleListView.as_view(),
        name='article-list-customer-insight',
    ),
    url(
        r"^finance/$",
        article.views.FinanceArticleListView.as_view(),
        name='article-list-finance',
    ),
    url(
        r"^business-planning/$",
        article.views.BusinessPlanningArticleListView.as_view(),
        name='article-list-business-planning',
    ),
    url(
        r"^getting-paid/$",
        article.views.GettingPaidArticleListView.as_view(),
        name='article-list-getting-paid',
    ),
    url(
        r"^operations-and-compliance/$",
        article.views.OperationsAndComplianceArticleListView.as_view(),
        name='article-list-operations-and-compliance',
    ),
    url(
        r"^market-research/doing-business-with-integrity/$",
        article.views.DoBusinessWithIntegrityView.as_view(),
        name='business-with-integrity',
    ),
    url(
        r"^market-research/do-research-first/$",
        article.views.DoResearchFirstView.as_view(),
        name='article-research-market',
    ),
    url(
        r"^market-research/define-market-potential/$",
        article.views.DefineMarketPotentialView.as_view(),
        name='define-market-potential',
    ),
    url(
        r"^market-research/research-your-market/$",
        article.views.DoFieldResearchView.as_view(),
        name='do-field-research',
    ),
    url(
        r"^market-research/analyse-the-competition/$",
        article.views.AnalyseTheCompetitionView.as_view(),
        name='analyse-the-competition',
    ),
    url(
        r"^market-research/visit-a-trade-show/$",
        article.views.VisitTradeShowView.as_view(),
        name='visit-trade-show',
    ),
    url(
        r"^market-research/know-the-relevant-legislation/$",
        article.views.KnowTheRelevantLegislationView.as_view(),
        name='know-the-relevant-legislation',
    ),
    url(
        r"^customer-insight/know-your-customers/$",
        article.views.KnowYourCustomerView.as_view(),
        name='know-your-customer',
    ),
    url(
        r"^customer-insight/meet-your-customers/$",
        article.views.MeetYourCustomerView.as_view(),
        name='meet-your-customers',
    ),
    url(
        r"^customer-insight/manage-language-differences/$",
        article.views.ManageLanguageDifferencesView.as_view(),
        name='manage-language-differences',
    ),
    url(
        r"^customer-insight/understand-your-customers-culture/$",
        article.views.UnderstandYourCustomersCultureView.as_view(),
        name='understand-your-customers-culture',
    ),
    url(
        r"^finance/get-money-to-export/$",
        article.views.GetMoneyToExportView.as_view(),
        name='get-money-to-export',
    ),
    url(
        r"^finance/choose-the-right-finance/$",
        article.views.ChooseTheRightFinanceView.as_view(),
        name='choose-right-finance',
    ),
    url(
        r"^finance/get-export-finance/$",
        article.views.GetExportFinanceView.as_view(),
        name='get-export-finance',
    ),
    url(
        r"^finance/raise-money-by-borrowing/$",
        article.views.RaiseMoneyByBorrowingView.as_view(),
        name='raise-money-by-borrowing',
    ),
    url(
        r"^finance/borrow-against-assets/$",
        article.views.BorrowAgainstAssetsView.as_view(),
        name='borrow-against-assets',
    ),
    url(
        r"^finance/raise-money-with-investment/$",
        article.views.RaiseMoneyWithInvestmentView.as_view(),
        name='raise-money-with-investment',
    ),
    url(
        r"^finance/get-finance-support-from-government/$",
        article.views.GetGovernmentFinanceSupportView.as_view(),
        name='get-finance-support-from-government',
    ),
    url(
        r"^business-planning/make-an-export-plan/$",
        article.views.MakeExportingPlanView.as_view(),
        name='make-an-export-plan',
    ),
    url(
        r"^business-planning/find-a-route-to-market/$",
        article.views.FindARouteToMarketView.as_view(),
        name='find-a-route-to-market',
    ),
    url(
        r"^business-planning/sell-overseas-directly/$",
        article.views.SellOverseasDirectlyView.as_view(),
        name='sell-overseas-directly',
    ),
    url(
        r"^business-planning/use-an-overseas-agent/$",
        article.views.UseOverseasAgentView.as_view(),
        name='use-an-overseas-agent',
    ),
    url(
        r"^business-planning/use-a-distributor/$",
        article.views.UseDistributorView.as_view(),
        name='use-a-distributor',
    ),
    url(
        r"^business-planning/choosing-an-agent-or-distributor/$",
        article.views.ChoosingAgentOrDistributorView.as_view(),
        name='choosing-an-agent-or-distributor',
    ),
    url(
        r"^business-planning/licensing-and-franchising/$",
        article.views.LicenceAndFranchisingView.as_view(),
        name='licensing-and-franchising',
    ),
    url(
        r"^business-planning/license-your-product-or-service/$",
        article.views.LicenceYourProductOrServiceView.as_view(),
        name='license-your-product-or-service',
    ),
    url(
        r"^business-planning/franchise-your-business/$",
        article.views.FranchiseYourBusinessView.as_view(),
        name='franchise-your-business',
    ),
    url(
        r"^business-planning/start-a-joint-venture/$",
        article.views.StartJointVentureView.as_view(),
        name='start-a-joint-venture',
    ),
    url(
        r"^business-planning/set-up-an-overseas-operation/$",
        article.views.SetupOverseasOperationView.as_view(),
        name='set-up-an-overseas-operation',
    ),
    url(
        r"^getting-paid/consider-how-youll-get-paid/$",
        article.views.ConsiderHowPaidView.as_view(),
        name='consider-how-youll-get-paid',
    ),
    url(
        r"^getting-paid/invoice-currency-and-contents/$",
        article.views.InvoiceCurrencyAndContentsView.as_view(),
        name='invoice-currency-and-contents',
    ),
    url(
        r"^getting-paid/decide-when-youll-get-paid/$",
        article.views.DecideWhenPaidView.as_view(),
        name='decide-when-youll-get-paid',
    ),
    url(
        r"^getting-paid/payment-methods/$",
        article.views.PaymentMethodsView.as_view(),
        name='payment-methods',
    ),
    url(
        r"^getting-paid/insure-against-non-payment/$",
        article.views.InsureAgainstNonPaymentView.as_view(),
        name='insure-against-non-payment',
    ),
    url(
        r"^operations-and-compliance/anti-bribery-and-corruption-training/$",
        article.views.AntiBriberyAndCorruptionTrainingView.as_view(),
        name='anti-bribery-and-corruption-training',
    ),
    url(
        r"^operations-and-compliance/plan-the-logistics/$",
        article.views.PlanTheLogisticsView.as_view(),
        name='plan-the-logistics',
    ),
    url(
        r"^operations-and-compliance/use-a-freight-forwarder/$",
        article.views.UseFreightForwarderView.as_view(),
        name='use-a-freight-forwarder',
    ),
    url(
        r"^operations-and-compliance/use-incoterms-in-contracts/$",
        article.views.UseIncotermsInContractsView.as_view(),
        name='use-incoterms-in-contracts',
    ),
    url(
        r"^operations-and-compliance/get-your-export-documents-right/$",
        article.views.GetYourExportDocumentsRightView.as_view(),
        name='get-your-export-documents-right',
    ),
    url(
        r"^operations-and-compliance/internationalise-your-website/$",
        article.views.InternationaliseWesbiteView.as_view(),
        name='internationalise-your-website',
    ),
    url(
        r"^operations-and-compliance/match-your-website-to-your-audience/$",
        article.views.MatchYourWebsiteToYourAudienceView.as_view(),
        name='match-your-website-to-your-audience',
    ),
    url(
        r"^operations-and-compliance/protect-your-intellectual-property/$",
        article.views.WhatIntellectualPropertyIsView.as_view(),
        name='what-intellectual-property-is',
    ),
    url(
        r"^operations-and-compliance/types-of-intellectual-property/$",
        article.views.TypesOfIntellectualPropertyView.as_view(),
        name='types-of-intellectual-property',
    ),
    url(
        r"^operations-and-compliance/know-what-ip-you-have/$",
        article.views.KnowWhatIntellectualPropertyYouHaveView.as_view(),
        name='know-what-IP-you-have',
    ),
    url(
        r"^operations-and-compliance/international-ip-protection/$",
        article.views.IntellectualPropertyProtectionView.as_view(),
        name='ip-protection-in-multiple-countries',
    ),
    url(
        r"^operations-and-compliance/report-corruption/$",
        article.views.ReportCorruptionView.as_view(),
        name='report-corruption',
    ),
    url(
        r"^new/next-steps/$",
        article.views.NextStepsNewExporterView.as_view(),
        name='next-steps-new-exporter',
    ),
    url(
        r"^occasional/next-steps/$",
        article.views.NextStepsOccasionalExporterView.as_view(),
        name='next-steps-occasional-exporter',
    ),
    url(
        r"^regular/next-steps/$",
        article.views.NextStepsRegularExporterView.as_view(),
        name='next-steps-regular-exporter',
    ),
    url(
        r'^triage/(?P<step>.+)/$',
        triage.views.TriageWizardFormView.as_view(
            url_name='triage-wizard', done_step_name='finished'
        ),
        name='triage-wizard'
    ),
    url(
        r'^triage/$',
        triage.views.TriageStartPageView.as_view(),
        name='triage-start'
    ),
    url(
        r'^custom/$',
        triage.views.CustomPageView.as_view(),
        name='custom-page'
    ),
    url(
        r'^api/internal/companies-house-search/$',
        triage.views.CompaniesHouseSearchApiView.as_view(),
        name='api-internal-companies-house-search'
    ),
    url(
        r'^story/hello-babys-rapid-online-growth/$',
        casestudy.views.CasestudyHelloBabyView.as_view(),
        name='casestudy-hello-baby'
    ),
    url(
        r'^story/online-marketplaces-propel-freestyle-xtreme-sales/$',
        casestudy.views.CasestudyMarketplaceView.as_view(),
        name='casestudy-online-marketplaces'
    ),
    url(
        r'^story/york-bag-retailer-goes-global-via-e-commerce/$',
        casestudy.views.CasestudyYorkBagView.as_view(),
        name='casestudy-york-bag'
    ),
    url(
        r'^healthcheck/api/$',
        healthcheck.views.APIProxyAPIView.as_view(),
        name='healthcheck-api'
    ),
    url(
        r'^healthcheck/single-sign-on/$',
        healthcheck.views.SingleSignOnAPIView.as_view(),
        name='healthcheck-single-sign-on'
    ),
    url(
        r'^contact-us/intro/$',
        contact.views.InterstitialView.as_view(service=None),
        name='contact-us-interstitial-service-agnostic',
    ),
    url(
        r'^contact-us/(?P<service>[-\w\d]+)/intro/$',
        contact.views.InterstitialView.as_view(),
        name='contact-us-interstitial-service-specific',
    ),
    url(
        r'^contact-us/(?P<service>[-\w\d]+)/$',
        contact.views.FeedbackWizardFormView.as_view(),
        name='contact-us-service-specific'
    ),
    url(
        r'^contact-us/$',
        contact.views.FeedbackWizardFormView.as_view(service=None),
        name='contact-us-service-agnostic'
    ),
    url(
        r'^contact-us/(?P<service>[-\w\d]+)/triage/$',
        contact.views.TriageWizardFormView.as_view(),
        name='contact-us-triage-wizard'
    ),
    url(
        r"^get-finance/$",
        finance.views.GetFinanceNegotiator.as_view(),
        name='get-finance'
    ),
    url(
        r'^get-finance/contact/thanks/$',
        finance.views.GetFinanceLeadGenerationSuccessView.as_view(),
        name='uk-export-finance-lead-generation-form-success'
    ),
    url(
        r'^get-finance/(?P<step>.+)/$',
        finance.views.GetFinanceLeadGenerationFormView.as_view(
            url_name='uk-export-finance-lead-generation-form',
            done_step_name='finished'
        ),
        name='uk-export-finance-lead-generation-form'
    ),
    url(
        r'^high-potential-opportunities/(?P<slug>[-\w\d]+)/contact/$',
        invest.views.HighPotentialOpportunityFormView.as_view(),
        name='high-potential-opportunity-request-form'
    ),
    url(
        r'^high-potential-opportunities/(?P<slug>[-\w\d]+)/$',
        invest.views.HighPotentialOpportunityDetailView.as_view(),
        name='high-potential-opportunity-details'
    ),
]

urlpatterns += redirects
