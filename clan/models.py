from django.db import models
from decimal import Decimal
from datetime import datetime
from django.urls import reverse
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils.crypto import get_random_string

# Create your models here.



##LIMIT USERS TO ONLY 15 CLANS
class Clan(models.Model):
    name            = models.CharField(max_length=55)
    location        =   models.CharField(max_length=150, default='Not yet specified')
    varients        = models.ManyToManyField(User, related_name="varients")
    chief            = models.ForeignKey(User, on_delete=models.PROTECT)
    trasurer        = models.ManyToManyField(User, related_name="trasurer", blank=True)
    main_balance    = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    credits         =   models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    interest        = models.DecimalField(default=20.00, decimal_places=2, max_digits=10)
    money_in_credits=   models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    total_interest  =   models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    revenue_share   =   models.DecimalField(default=0.00, max_digits=10, decimal_places=2)



    slug            = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    created_on      = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('clan-detail', kwargs={'slug': self.slug})
    
    def get_absolute_url_profile(self):
        return reverse('clan-update', kwargs={'slug': self.slug})
    
    def get_absolute_url_credit_list(self):
        return reverse('credit_list', kwargs={'slug': self.slug})
    


class Varient(models.Model):
    STATUS = (
        ('chief','chief'),
        ('treasurer','treasurer'),
        ('varient','varient')
    )
    clan    =   models.ForeignKey(Clan, on_delete=models.PROTECT, related_name="clan")
    varient =   models.ForeignKey(User, on_delete=models.PROTECT, related_name="varient")
    revenue_share = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    show_saving   = models.BooleanField(default=True)
    saving =   models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status  =   models.CharField(choices=STATUS, max_length=9, default='varient')

    
    add_on  =   models.DateTimeField(auto_now_add=True)

    def get_varient_settings_url(self):
        return reverse('varient_settings', kwargs={'id': self.id})

    def update_revenue_share(self, amount):
        self.revenue_share += Decimal.from_float(int(amount))
        self.save()


    def __str__(self):
        return f'{self.varient.get_full_name()}'
    


class ClanSettings(models.Model):
    WHO_CAN_SEE_CREDITS = [
        ('everyone','Everyone'),
        ('staff','Trassurers and Chief')
    ]
    clan                        =   models.OneToOneField(Clan, on_delete=models.CharField)
    who_can_see_credits         =   models.CharField(choices=WHO_CAN_SEE_CREDITS, default='everyone', max_length=25)
    minimum_in_savings_for_credit = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    maximum_member_savings      =   models.DecimalField(decimal_places=2, default=10000, max_digits=10)
    maximum_credit              =   models.DecimalField(decimal_places=2, default=5000, max_digits=10)
    max_members                 =   models.PositiveIntegerField(default=20)
    interest                    =   models.DecimalField(default=20, decimal_places=2, max_digits=10)


    



class ClanSaving(models.Model):
    paid_by     =   models.ForeignKey(Varient, on_delete=models.CASCADE)
    saved_by    =   models.ForeignKey(Varient, on_delete=models.CASCADE, related_name='saved_by')
    clan        =   models.ForeignKey(Clan, on_delete=models.CASCADE)
    amount      =   models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    saved_on    =   models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.clan) + str(self.amount)

    


class ClanActivity(models.Model):
    ACTION_CHOICES = [
        ('CLAN_CREATED', 'Clan Created'),
        ('SAVINGS_ADDED', 'Savings Added'),
        ('VARIENT_ADDED', 'Varient Added'),
        ('CREDIT_APPROVED', 'CREDIT Approved'),
    ]

    clan = models.ForeignKey('Clan', on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities_performed')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)  # Optional details about the activity
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} - {self.clan.name} by {self.user or 'System'} on {self.timestamp}"





class ClanCredit(models.Model):
    PERIOD = [
        ('12','1 Week'),
        ('20', '2 Weeks'),
        ('25', '25% 1Month'),
        ('30', '1 Month'),
        ('40','8 Weeks'),
        ('50', '12 Weeks')
    ]
    STATUS_CHOICES = [
        ('pending_approval','pending'),
        ('denied','Denied'),
        ('payment','Payment'),
        ('paid','Paid'),
        ('overdue','Overdue')
    ]
    clan        =   models.ForeignKey('Clan', on_delete=models.CASCADE)
    credited_by =   models.ForeignKey(Varient, on_delete=models.PROTECT, blank=True, related_name='credited_by')
    approved_by =   models.ForeignKey(Varient, models.CASCADE, blank=True, null=True)
    amount      =   models.DecimalField(decimal_places=2, default=0.00, max_digits=7)
    amount_paid =   models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    total_amount=   models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    balance     =   models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    interest    =   models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    status      =   models.CharField(choices=STATUS_CHOICES, default='pending_approval', max_length=20)
    paid        =   models.BooleanField(default=False)
    percentage  =   models.CharField(choices=PERIOD, default='30', max_length=3)

    approved    =   models.BooleanField(default=False)
    date_approved   = models.DateTimeField(auto_now=True)
    date_applied    = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(blank=True, unique=True,max_length=20, null=True)


    def save(self, *args, **kwargs):
        self.interest = Decimal.from_float(int(self.percentage))/100 * self.amount
        self.total_amount = self.interest + self.amount
        self.balance = self.interest + self.amount - Decimal.from_float(float(self.amount_paid))
        if self.paid == False and self.amount_paid == self.total_amount:
            self.paid = True
            

            
 
        super().save(*args, **kwargs)


    def distribute_interest(self):
        clan = Clan.objects.get(id=self.clan.id)
        credit = ClanCredit.objects.get(id=self.id)
        if self.paid:
            total_interest = self.amount * int(self.percentage) / 100
            borrower_share = float(total_interest) * 0.5
            shared_interest = float(total_interest) * 0.5
            varients = Varient.objects.filter(clan=self.credited_by.clan)
            total_savings = sum(varient.saving for varient in varients)
            
            
            for varient in varients:
                share_ratio = varient.saving / total_savings if total_savings > 0 else 0
                share_amount = Decimal.from_float(shared_interest) * share_ratio
                RevenueShare.objects.create(varient=varient, revenue_amount=share_amount)
                varient.update_revenue_share(share_amount)
            
            RevenueShare.objects.create(clan=clan, credit=credit, varient=self.credited_by, revenue_amount=borrower_share)
            self.credited_by.update_revenue_share(borrower_share)

    def __str__(self):
        return str(self.credited_by)
    
    def get_absolute_url(self):
        return reverse('clan-credit-details', kwargs={'id': self.id})
    



class ClanPaymentLoan(models.Model):
    credit  = models.ForeignKey(ClanCredit, on_delete=models.PROTECT)
    paid_by =   models.ForeignKey(User, on_delete=models.PROTECT)
    amount  =   models.DecimalField(max_digits=8, decimal_places=2)
    created_on = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.amount + self.credit.amount_paid == self.credit.total_amount and self.credit.paid == False:
            self.credit.paid = True
            self.credit.status = 'paid'
            self.credit.save()
            self.credit.distribute_interest()

            #Increase clan total interests if credit is fully paid
            clan = Clan.objects.get(id=self.credit.clan.id)
            clan.total_interest += self.credit.interest
            clan.money_in_credits += self.credit.interest
            clan.save()

    def __str__(self):
        return f"{self.paid_by.get_full_name()} - {self.amount}"
    


@receiver(post_save, sender=ClanPaymentLoan)
def payLoanSignal(sender, instance, created, **kwargs):
    if created:
        obj = ClanCredit.objects.get(id=instance.credit.id)
        clan = Clan.objects.get(id=obj.clan.id)
        clan.main_balance += instance.amount

        clan.money_in_credits = max(clan.money_in_credits - instance.amount, Decimal("0.00"))

        '''
        try:
            clan.money_in_credits -= instance.amount
            #if clan.money_in_credits < 0.00:
                #clan.money_in_credits = 0.00
        except:
            clan.money_in_credits = 0.00
        '''
        
        clan.save()


        ##REDUCE BALANCE
        obj.amount_paid += instance.amount
        obj.save()





class RevenueShare(models.Model):
    clan        =   models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True)
    credit      =   models.ForeignKey(ClanCredit, on_delete=models.CASCADE, null=True, blank=True)
    varient     =   models.ForeignKey(Varient, on_delete=models.CASCADE)
    revenue_amount     =   models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_out    =   models.BooleanField(default=False)
    created_on  =   models.DateTimeField(auto_now_add=True)


    







def generate_unique_slug(instance):
    base_slug = slugify(instance.name)
    slug = base_slug
    ModelClass = instance.__class__

    # Check if slug is unique
    counter = 1
    while ModelClass.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)

pre_save.connect(pre_save_product_receiver, sender=Clan)
