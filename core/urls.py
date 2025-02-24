from django.urls import path
from .views import (
    home,
    contact_support,
    MyLoanslistProfile,
    MyLoanslistUser,
    UnApprovedLoanslist,
    LoanDetailView,

    search_witness,

    WitnessRevenueList
)

urlpatterns = [
    path('', home, name="home"),
    path('support', contact_support, name="contact"),
    path('loan-list/unapproved', UnApprovedLoanslist.as_view(), name="credit-list"),
    path('loan-details/<int:pk>', LoanDetailView.as_view(), name="loan-detail"),
    path('my-loan-list/profile', MyLoanslistProfile.as_view(), name="my-credit-list-profile"),
    path('my-loan-list/user', MyLoanslistUser.as_view(), name="my-credit-list-user"),
    path('search_user/', search_witness, name="search_user"),

    path('credit/witness_revenue/', WitnessRevenueList.as_view(), name='witness_revenue')
]

