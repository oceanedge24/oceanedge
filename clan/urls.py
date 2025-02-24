from django.urls import path
from .views import (
    clanListFormView, ClanDeleteView,
    VarientDetailView, VarientDeleteView, search_users, add_user_to_clan, clan_detail_view,
    clan_activities,credit_details,approve_credit,
    credit_list,apply_for_credit,update_Clan_page,clanProfileForm,
    varient_settings,)


urlpatterns = [
    path('clan-list', clanListFormView, name="clan_list"),
    path('<str:slug>/', clan_detail_view, name="clan-detail"),
    path('clan/<str:slug>/search_users/', search_users, name='search_users'),
    path('clan/<int:pk>/varient/', VarientDetailView.as_view(), name="clan-varient-details"),
    path('clan/<str:slug>/<int:id>/add-varient/', add_user_to_clan, name='add_user_to_clan'),
    path("json/<str:slug>/", clanProfileForm, name="update_clan"),
    path("<str:slug>/info", update_Clan_page, name="clan-update"),

    path('<str:slug>/delete/', ClanDeleteView.as_view(), name='delete_clan'),
    path('varient/<int:pk>/delete/', VarientDeleteView.as_view(), name="varient-delete"),

    path('<str:slug>/activities', clan_activities, name='activities'),

    path('clan/<str:slug>/credit_list/', credit_list, name='credit_list'),
    path('clan/<str:slug>/loan_request/', apply_for_credit, name='apply_for_credit'),
    path('credit/<int:id>/', credit_details, name='clan-credit-details'),
    path('<int:pk>/credit-approve/', approve_credit, name='approve_clan_credit'),

    path('varient/settings/<int:id>/', varient_settings, name='varient_settings'),
]