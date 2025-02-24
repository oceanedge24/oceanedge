from typing import Any, Dict, Optional
from django.db.models import Q
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, View, FormView, DeleteView
from account.models import User
from django.db import transaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .models import Clan, Varient, ClanSaving, ClanActivity, ClanCredit, ClanPaymentLoan, ClanSettings
from .forms import (ClanCreateForm, SavingForm, ClanUpdateForm,
                    ClanApplyLoan, LoanPaymentForm, ShowTotalSavingsForm,
                    ClanSettingsForm)
# Create your views here.



@login_required()
def clanListFormView(req):
    user = req.user
    objs = Clan.objects.filter(varients=user)
    form = ClanCreateForm()

    form = ClanCreateForm(req.POST)
    if form.is_valid():
        if user.max_clan_create <= Clan.objects.filter(chief = user).count():
            messages.add_message(req, messages.INFO, "User reached maximum count")
            return redirect('clan_list')

        else:
            name = form.cleaned_data.get('name')
            obj = Clan.objects.create(
                    name = name,
                    chief = req.user,
                )
            obj.trasurer.add(req.user)
            obj.save()
            
            ### UPDATE ACTIVITIES
            ClanActivity.objects.create(
                clan=obj,
                user=user,
                action='CLAN_CREATED',
                details=f"Clan '{name}' was created by '{user}."
    )
            
            #Add Clan Creator To Clan
            obj.varients.add(req.user)
            #create_varient_instance
            obj_varient = Varient.objects.get_or_create(
                    clan = obj,
                    varient = req.user,
                    status = 'chief'
                )
            return redirect(obj.get_absolute_url())

    context = {
        'objs':objs,
        'form':form
    }
    return render(req, 'clan/clan_list.html', context)



@login_required
def clan_detail_view(request, slug):
    object = get_object_or_404(Clan, slug=slug)
    varients = Varient.objects.filter(clan=object).order_by('-saving')


    ## Add Savings to clan
    if request.method == 'POST':
        form = SavingForm(object, request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = form.cleaned_data['user']

            ### Check if user is chief of clan
            varient = Varient.objects.get(clan=object, varient=user)
            if not (request.user in object.trasurer.all() or request.user == object.chief):
                messages.error(request, 'You\'re not authorised to add savings!')
                return redirect(object.get_absolute_url())
                

            # Clan Saving Info
            ClanSaving.objects.create(
                clan = object,
                saved_by = Varient.objects.get(clan=object, varient=user),
                paid_by = Varient.objects.get(clan=object, varient=request.user),
                amount = amount
            )
            # Increase Clan amount
            object.main_balance  += amount
            object.save()

            # Add user savings
            
            member = Varient.objects.get(clan=object, varient=user)
            member.saving += amount
            member.save()

            
            ##UPDATE ACTIVITY
            ClanActivity.objects.create(
                clan=object,
                user=request.user,
                action='SAVINGS_ADDED',
                details=f"An amount of K{amount} was saved by {member}."
            )
            return redirect(object.get_absolute_url())

    else:
        form = SavingForm(object)

    context = {
        'varients': varients,
        'object': object,
        'form': form
    }
    return render(request, 'clan/clan-detail.html', context)




class ClanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Clan
    success_url = 'clan_list'


    def test_func(self):
        obj = self.get_object()
        if obj.chief == self.request.user:
            return True
        return False


def search_users(request, slug):
    clan = get_object_or_404(Clan, slug=slug)
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(mobile_number__icontains=query) | Q(id_number__icontains=query)
        ).exclude(
                id__in=clan.varients.all().values_list('id', flat=True)
            )
    else:
        users = User.objects.none()

    context = {
        'clan': clan,
        'query': query,
        'users': users
    }
    return render(request, 'clan/search_users_results.html', context)




class VarientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Varient
    template_name = 'clan/clan-varient-detail.html'
    

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if obj.varient.id == user.id or user in obj.clan.trasurer.all() or user.id == obj.clan.chief.id:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['savings'] = ClanSaving.objects.filter(saved_by = obj).order_by('-saved_on')
        return context

    

class VarientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Varient
    template_name = 'clan/varient_delete.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if obj.varient.id == user.id or user.id == obj.clan.chief.id:
            return True
        return False
    
    def form_valid(self, form):
        if self.object.saving > 10.00:
            messages.error(self.request, '''Cannot delete member with savings greater than K 10.00.
                        Please contact the Clan's chief or Trasurer for help.''')
            return redirect('member_settings', member_id=self.object.id)
        return super().form_valid(form)

def add_user_to_clan(request, slug, id):
    clan = get_object_or_404(Clan, slug=slug)
    varient = get_object_or_404(User, pk=id)
    clan.varients.add(varient)
    Varient.objects.get_or_create(
        clan = clan,
        varient = varient,
    )
    ##UPDATE ACTIVITY
    ClanActivity.objects.create(
        clan=clan,
        user=request.user,
        action='VARIENT_ADDED',
        details=f"New Varient {varient} was added by'{request.user}'."
        )
    return redirect(clan.get_absolute_url())



from django.core.paginator import Paginator


@login_required
def clan_activities(request, slug):
    clan = get_object_or_404(Clan, slug=slug)
    activities = clan.activities.order_by('-timestamp')

    # Paginate the activities (e.g., 10 activities per page)
    paginator = Paginator(activities, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clan/clan_activities.html', {'clan': clan, 'page_obj': page_obj})



@login_required
@require_POST
def clanProfileForm(request, slug):
    clan =get_object_or_404(Clan, slug=slug)
    form = ClanUpdateForm(request.POST, instance=clan)
    settings = get_object_or_404(ClanSettings, clan__id = clan.id)

    settings_form = ClanSettingsForm(request.POST, instance=settings)

    if form.is_valid() and settings_form.is_valid():
        clan = form.save()
        settings_form.save()
        
        new_url = reverse("clan-update", kwargs={"slug": clan.slug})
 
        return JsonResponse({
            "success": True,
            "message": "Profile Clan Updated Successfully!",
            "redirect_url": new_url
            
        })

    else:
        errors = {
            'form_errors': form.errors,
            'settings_form_errors': settings_form.errors,
        }
        

    context = {
        'object':clan,
        'form':form,
        'settings_form': settings_form,
    }
  



@ensure_csrf_cookie  # Ensure CSRF cookie is set when rendering the page
def update_Clan_page(request, slug):
    clan = get_object_or_404(Clan, slug=slug)
    settings = get_object_or_404(ClanSettings, clan__id = clan.id)

    initial_data = {
            'max_members': settings.max_members,
            'who_can_see_credits': settings.who_can_see_credits,
            'minimum_in_savings_for_credit': settings.minimum_in_savings_for_credit
        }
    
    settings_form = ClanSettingsForm(initial=initial_data)
    form = ClanUpdateForm(instance=clan)
    
    context = {
        'object':clan,
        'form':form,
        'settings_form':settings_form
    }
    return render(request, 'clan/clan_profile_view.html', context)




#####################CREDIT

@login_required
def credit_list(request, slug):
    clan = get_object_or_404(Clan, slug=slug)
    credit_obj = ClanCredit.objects.filter(clan=clan).order_by('-date_applied')
    if clan.clansettings.who_can_see_credits == "everyone":
        context = {
        'object':clan,
        'credit_obj':credit_obj
    }
        
    elif clan.clansettings.who_can_see_credits == "staff":
        if request.user.id == clan.chief.id or request.user in clan.trasurer.all():
            context = {
                'object':clan,
                'credit_obj':credit_obj
            }
        
    
    else:
        messages.error(request, "you're not allowed to view this page")
        return redirect(clan.get_absolute_url())
    
    
    return render(request, 'clan/credit_list.html', context)



@login_required()
def apply_for_credit(request, slug):
    object = get_object_or_404(Clan, slug=slug)
    user = request.user
    credited_by = Varient.objects.get(varient=user, clan=object)
    form = ClanApplyLoan()
    if request.method == 'POST':
        form = ClanApplyLoan(request.POST)
        if form.is_valid():
            obj_created = ClanCredit.objects.create(
                clan = object,
                credited_by = credited_by,
                amount = Decimal.from_float(float(form.cleaned_data['amount'])),
                status  = 'pending_approval',
                percentage = form.cleaned_data.get('period')
            )   
            #return redirect(obj_created.get_absolute_url())
            return redirect(object.get_absolute_url_credit_list())
    return render(request, 'clan/clan_loan_request.html', {'form':form})





@login_required()
@transaction.atomic
def approve_credit(request, pk):
    user = request.user
    obj = get_object_or_404(ClanCredit,pk=pk)
    obj.approved_by
    if obj.clan.chief == request.user or request.user in obj.clan.trasurer.all():
        if obj.amount <= obj.clan.main_balance:
            if obj.approved == False:
                obj.approved = True
                obj.status = 'payment'
                approved_by = user
                obj.approved_by = approved_by
                obj.save()


                ####ADD CLAN ACTIVITY
                ClanActivity.objects.create(
                    clan = obj.clan,
                    user = user,
                    action = 'CREDIT_APPROVED',
                    details = f"Credit of {obj.amount} by {obj.credited_by } was approved"
                )

                #### INCREASE CLAN's MONEY IN CREDITS
                get_clan = obj.clan
                get_clan.money_in_credits += obj.amount
                get_clan.main_balance -= obj.amount
                get_clan.save()

                return redirect(obj.get_absolute_url())
        else:
            messages.add_message(request, messages.INFO, 'You dont have enough money in your savings')
    else:
            messages.add_message(request, messages.INFO, 'Contact Clan Chief or Trasurer for approval')
    return redirect(obj.get_absolute_url())



@login_required()
@transaction.atomic
def credit_details(request, id):
    object = get_object_or_404(ClanCredit, id=id)
    payments = ClanPaymentLoan.objects.filter(credit=object)
    clan_id = object.clan.id
    clan = Clan.objects.get(id=clan_id)
    form = LoanPaymentForm()

    if request.method == "POST":
        form = LoanPaymentForm(request.POST)
        if request.user == clan.chief or request.user in clan.trasurer.all():
            
                if form.is_valid():
                    amount = Decimal.from_float(float(form.cleaned_data['amount']))
                    if amount <= object.balance:
                        ClanPaymentLoan.objects.create(
                            credit = object,
                            paid_by = request.user,
                            amount = Decimal.from_float(float(form.cleaned_data['amount']))
                        )
                        return redirect(object.get_absolute_url())
                    else:
                        messages.add_message(request, messages.INFO, "You Can't over pay your loan")
        else:
            messages.add_message(request, messages.INFO, "You can perform this operation, contact trasurer or chief")
            return redirect(object.get_absolute_url())
        
    context = {
        'obj':object,
        'payments':payments,
        'form':form
    }
    return render(request, 'clan/clan-credit-details.html', context)


import logging
from django.db import models
logger = logging.getLogger(__name__)


@login_required
def varient_settings(request, id):
    varient = Varient.objects.get(varient=request.user, id=id)
    if request.method == 'POST':
        form = ShowTotalSavingsForm(request.POST, instance=varient)
        if form.is_valid():
            form.save()
            return redirect(varient.get_varient_settings_url())
    else:
        form = ShowTotalSavingsForm(instance=varient)
    return render(request, 'clan/varient_settings.html', {'form': form, 'object':varient})


