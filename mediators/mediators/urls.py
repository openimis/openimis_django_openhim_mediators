from django.contrib import admin
from django.urls import path
from claim_mediator.views import getClaims
from coverage_mediator.views import getCoverage
from organisation_mediator.views import getOrganisation
from patient_mediator.views import getPatient
from claimresponse_mediator.views import getClaimResponse
from coverageeligibilityrequest_mediator.views import getCoverageEligibilityRequest
from coverage_mediator.views import registerCoverageMediator
from claim_mediator.views import registerClaimsMediator
from organisation_mediator.views import registerOrganisationMediator
from patient_mediator.views import registerPatientMediator
from claimresponse_mediator.views import registerClaimResponseMediator
from coverageeligibilityrequest_mediator.views import registerCoverageEligibilityRequestMediator
from overview.views import congifgurations
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Claim', getClaims),
    path('Coverage', getCoverage),
    path('Organisation', getOrganisation),
    path('Patient', getPatient),
    path('CoverageEligibilityRequest', getCoverageEligibilityRequest),
    path('ClaimResponse',getClaimResponse)
]

congifgurations()
registerClaimsMediator()
registerCoverageMediator()
registerOrganisationMediator()
registerPatientMediator()
registerClaimResponseMediator()
registerCoverageEligibilityRequestMediator()