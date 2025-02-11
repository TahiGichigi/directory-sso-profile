import directory_healthcheck.views

from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import include, url
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

import core.views
import enrolment.views
import profile.eig_apps.views
import profile.exops.views
import profile.fab.views
import profile.soo.views


def company_required(function):
    inner = user_passes_test(
        lambda user: bool(user.company),
        reverse_lazy('find-a-buyer'),
    )
    if function:
        return login_required(inner(function))


healthcheck_urls = [
    url(
        r'^$',
        directory_healthcheck.views.HealthcheckView.as_view(),
        name='healthcheck'
    ),
    url(
        r'^ping/$',
        directory_healthcheck.views.PingView.as_view(),
        name='ping'
    ),
]

api_urls = [
    url(
        r'^v1/companies-house-search/$',
        core.views.CompaniesHouseSearchAPIView.as_view(),
        name='companies-house-search'
    ),
    url(
        r'^v1/postcode-search/$',
        core.views.AddressSearchAPIView.as_view(),
        name='postcode-search'
    ),

]


urlpatterns = [
    url(
        r'^api/',
        include(api_urls, namespace='api', app_name='api')
    ),
    url(
        r'^healthcheck/',
        include(
            healthcheck_urls, namespace='healthcheck', app_name='healthcheck'
        )
    ),
    url(
        r'^$',
        profile.eig_apps.views.LandingPageView.as_view(),
        name='index'
    ),
    url(
        r'^about/$',
        profile.eig_apps.views.AboutView.as_view(),
        name='about'
    ),
    url(
        r'^selling-online-overseas/$',
        login_required(profile.soo.views.SellingOnlineOverseasView.as_view()),
        name='selling-online-overseas'
    ),
    url(
        r'^export-opportunities/applications/$',
        login_required(
            profile.exops.views.ExportOpportunitiesApplicationsView.as_view()
        ),
        name='export-opportunities-applications'
    ),
    url(
        r'^export-opportunities/email-alerts/$',
        login_required(
            profile.exops.views.ExportOpportunitiesEmailAlertsView.as_view()
        ),
        name='export-opportunities-email-alerts'
    ),
    url(
        r'^enrol/$',
        enrolment.views.EnrolmentStartView.as_view(),
        name='enrolment-start'
    ),
    url(
        r'^enrol/business-type/$',
        enrolment.views.BusinessTypeRoutingView.as_view(),
        name='enrolment-business-type'
    ),
    url(
        r'^enrol/business-type/companies-house/(?P<step>.+)/$',
        enrolment.views.CompaniesHouseEnrolmentView.as_view(
            url_name='enrolment-companies-house',
            done_step_name='finished'
        ),
        name='enrolment-companies-house'
    ),
    url(
        r'^enrol/business-type/non-companies-house-company/(?P<step>.+)/$',
        enrolment.views.NonCompaniesHouseEnrolmentView.as_view(
            url_name='enrolment-sole-trader',
            done_step_name='finished'
        ),
        name='enrolment-sole-trader'
    ),
    url(
        r'^enrol/business-type/individual/start/$',
        enrolment.views.IndividualUserEnrolmentInterstitial.as_view(),
        name='enrolment-individual-interstitial'
    ),
    url(
        r'^enrol/business-type/individual/(?P<step>.+)/$',
        enrolment.views.IndividualUserEnrolmentView.as_view(
            url_name='enrolment-individual',
            done_step_name='finished'
        ),
        name='enrolment-individual'
    ),
    url(
        r'^enrol/business-type/overseas-business/$',
        enrolment.views.EnrolmentOverseasBusinessView.as_view(),
        name='enrolment-overseas-business'
    ),
    url(
        r'^enrol/pre-verified/(?P<step>.+)/$',
        enrolment.views.PreVerifiedEnrolmentView.as_view(
            url_name='enrolment-pre-verified',
            done_step_name='finished'
        ),
        name='enrolment-pre-verified'
    ),
    url(
        r'^enrol/pre-verified/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'enrolment-pre-verified', kwargs={'step': 'user-account'}
            ),
            query_string=True,
        )
    ),
    url(
        r'^enrol/resend-verification/(?P<step>.+)/$',
        enrolment.views.ResendVerificationCodeView.as_view(
            url_name='resend-verification',
            done_step_name='finished'
        ),
        name='resend-verification'
    ),
    url(
        r'^find-a-buyer/$',
        login_required(
            profile.fab.views.FindABuyerView.as_view(),
            login_url=reverse_lazy('enrolment-start'),
        ),
        name='find-a-buyer'
    ),
    url(
        r'^find-a-buyer/social-links/$',
        company_required(profile.fab.views.SocialLinksFormView.as_view()),
        name='find-a-buyer-social'
    ),
    url(
        r'^find-a-buyer/email/$',
        company_required(profile.fab.views.EmailAddressFormView.as_view()),
        name='find-a-buyer-email'
    ),
    url(
        r'^find-a-buyer/description/$',
        company_required(profile.fab.views.DescriptionFormView.as_view()),
        name='find-a-buyer-description'
    ),
    url(
        r'^find-a-buyer/website/$',
        company_required(profile.fab.views.WebsiteFormView.as_view()),
        name='find-a-buyer-website'
    ),
    url(
        r'^find-a-buyer/logo/$',
        company_required(profile.fab.views.LogoFormView.as_view()),
        name='find-a-buyer-logo'
    ),

    url(
        r'^find-a-buyer/personal-details/$',
        login_required(profile.fab.views.PersonalDetailsFormView.as_view()),
        name='find-a-buyer-personal-details'
    ),
    url(
        r'^find-a-buyer/publish/$',
        company_required(profile.fab.views.PublishFormView.as_view()),
        name='find-a-buyer-publish'
    ),
    url(
        r'^find-a-buyer/business-details/$',
        company_required(profile.fab.views.BusinessDetailsFormView.as_view()),
        name='find-a-buyer-business-details'
    ),
    url(
        r'^find-a-buyer/case-study/(?P<id>[0-9]+)/(?P<step>.+)/$',
        company_required(
            profile.fab.views.CaseStudyWizardEditView.as_view(
                url_name='find-a-buyer-case-study-edit'
            )
        ),
        name='find-a-buyer-case-study-edit'
    ),
    url(
        r'^find-a-buyer/case-study/(?P<step>.+)/$',
        company_required(
            profile.fab.views.CaseStudyWizardCreateView.as_view(
                url_name='find-a-buyer-case-study'
            )
        ),
        name='find-a-buyer-case-study'
    ),
    url(
        r'^find-a-buyer/add-expertise/$',
        company_required(profile.fab.views.ExpertiseRoutingFormView.as_view()),
        name='find-a-buyer-expertise-routing'
    ),
    url(
        r'^find-a-buyer/add-expertise/regions/$',
        company_required(
            profile.fab.views.RegionalExpertiseFormView.as_view()
        ),
        name='find-a-buyer-expertise-regional'
    ),
    url(
        r'^find-a-buyer/add-expertise/countries/$',
        company_required(profile.fab.views.CountryExpertiseFormView.as_view()),
        name='find-a-buyer-expertise-countries'
    ),
    url(
        r'^find-a-buyer/add-expertise/industries/$',
        company_required(
            profile.fab.views.IndustryExpertiseFormView.as_view()
        ),
        name='find-a-buyer-expertise-industries'
    ),
    url(
        r'^find-a-buyer/add-expertise/languages/$',
        company_required(
            profile.fab.views.LanguageExpertiseFormView.as_view()
        ),
        name='find-a-buyer-expertise-languages'
    ),
    url(
        r'^find-a-buyer/products-and-services/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'find-a-buyer-expertise-products-services-routing'
            ),
        ),
        name='find-a-buyer-products-and-services'
    ),
    url(
        r'^find-a-buyer/add-expertise/products-and-services/$',
        company_required(
            profile.fab.views.ProductsServicesRoutingFormView.as_view()
        ),
        name='find-a-buyer-expertise-products-services-routing'
    ),
    url(
        r'^find-a-buyer/add-expertise/products-and-services/other/$',
        company_required(
            profile.fab.views.ProductsServicesOtherFormView.as_view()
        ),
        name='find-a-buyer-expertise-products-services-other'
    ),
    url(
        (
            r'^find-a-buyer/add-expertise/products-and-services/'
            r'(?P<category>.+)/$'
        ),
        company_required(profile.fab.views.ProductsServicesFormView.as_view()),
        name='find-a-buyer-expertise-products-services'
    ),
    url(
        r'^find-a-buyer/admin/$',
        company_required(profile.fab.views.AdminToolsView.as_view()),
        name='find-a-buyer-admin-tools'
    ),
]

urlpatterns = [
    url(
        r'^profile/',
        include(urlpatterns)
    )
]
