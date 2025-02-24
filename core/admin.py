from django.contrib import admin
from .models import Credit, AproveCredit, PayLoan, LoanWitnessRevenue
# Register your models here.




admin.site.register(Credit)
admin.site.register(AproveCredit)
admin.site.register(PayLoan)
admin.site.register(LoanWitnessRevenue)


