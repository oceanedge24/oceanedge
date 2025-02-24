from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View, DetailView, FormView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

from account.models import Profile
from .models import Credit, PayLoan, AproveCredit, LoanWitnessRevenue
from .forms import ApplyLoanForm, LoanPaymentForm
from clan.models import Clan


User = get_user_model()


@login_required
def home(request):
    user = request.user
    clan = Clan.objects.filter(varients=user).distinct()[:12]
    
    context = {
        'clan':clan,
    }
    return render(request, 'home.html', context)



@login_required
def contact_support(request):
    return render(request, 'contact_support.html')
    





class UnApprovedLoanslist(LoginRequiredMixin, ListView):
    template_name = "my-credit-list.html"
    paginate_by =25

    def get_queryset(self):
        user = self.request.user
        qs = Credit.objects.filter(status = 'pending_approval').order_by('-applied_on')
        return qs

class MyLoanslistProfile(LoginRequiredMixin, ListView):
    template_name = "my-credit-list.html"
    paginate_by =25

    def get_queryset(self):
        user = self.request.user
        qs = Credit.objects.filter(approved_by = user.profile).order_by('-applied_on')
        return qs
    

class MyLoanslistUser(LoginRequiredMixin, ListView):
    template_name = "my-credit-list.html"
    paginate_by =25

    def get_queryset(self):
        user = self.request.user
        qs = Credit.objects.filter(creditor = user).order_by('-applied_on')
        return qs


########################## CREDIT DETAIL VIEW
class LoanDisplayView(LoginRequiredMixin, DetailView):
    model = Credit
    template_name = 'loan_detail.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoanPaymentForm
        context['payments'] = PayLoan.objects.filter(credit=self.get_object())
        return context

class LoanPayView(UserPassesTestMixin, FormView):
    form_class = LoanPaymentForm
   

    def test_func(self):
        obj = Credit.objects.get(pk=self.kwargs['pk'])
        if self.request.user.id == obj.approved_by.user.id:
            return True
        return False

    def form_valid(self, form):
        form.instance.paid_by = self.request.user
        form.instance.credit = Credit.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('loan-detail', kwargs={'pk': self.kwargs['pk']})
    

class LoanDetailView(View):
    def get(self, request, *args, **kwargs):
        view = LoanDisplayView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = LoanPayView.as_view()
        return view(request, *args, **kwargs)



from django.db.models import Q



def search_witness(request):
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        user = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) |
        Q(mobile_number__icontains=query) | Q(id_number__icontains=query)).first()
        if user:
            data = {
                'username': user.get_full_name(),
                'id_number': user.id_number
                # Add other user information you want to send to the front-end
            }
        else:
            data = {}
        return JsonResponse(data)
    



#Witness

class WitnessRevenueList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        qs = LoanWitnessRevenue.objects.filter(witness = self.request.user)
        return qs