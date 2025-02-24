from django.contrib import admin
from .models import (
    ClanSaving, Clan, Varient, ClanActivity, ClanCredit,ClanPaymentLoan, RevenueShare,
    ClanSettings
    )
# Register your models here.


admin.site.register(Varient)
admin.site.register(ClanSaving)
admin.site.register(Clan)
admin.site.register(ClanSettings)
admin.site.register(ClanActivity)
admin.site.register(ClanCredit)
admin.site.register(ClanPaymentLoan)
admin.site.register(RevenueShare)