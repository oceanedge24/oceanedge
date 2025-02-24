from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import Profile
from django.shortcuts import get_object_or_404
# Create your models here.


User = get_user_model()

class Credit(models.Model):
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
    creditor    =   models.ForeignKey(User, on_delete=models.PROTECT)
    percentage  =   models.CharField(choices=PERIOD, default='30', max_length=3)
    status      =   models.CharField(choices=STATUS_CHOICES, default='pending_approval', max_length=20)

    amount      =   models.DecimalField(max_digits=7, decimal_places=2)
    interest    =   models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    total_amount=   models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    amount_paid =   models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    balance     =   models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    approved    =   models.BooleanField(default=False)
    paid        =   models.BooleanField(default=False)
    approved_by =   models.ForeignKey(Profile,on_delete=models.PROTECT,
                        null=True, blank=True, related_name="approved_by"
                        )
    
    #1st Witness/Guaranter
    witness_1   =   models.ForeignKey(User, on_delete=models.CASCADE,
                                      null=True, blank=True,
                                      related_name="witness_1"
                                      )
    #2nd Witness/Guaranter
    witness_2_full_name   =   models.CharField(max_length=30, blank=True)
    witness_2_NRC_number   =    models.CharField(max_length=12, blank=True)
    witness_2_phone_number =  models.CharField(max_length=12, blank=True)

    applied_on  =   models.DateTimeField(default=timezone.now)
    approved_on =   models.DateTimeField(default=timezone.now)#auto_now_add=True, null=True, blank=True


    def save(self, *args, **kwargs):
        self.interest = Decimal.from_float(int(self.percentage))/100 * self.amount
        self.total_amount = self.interest + self.amount
        self.balance = self.interest + self.amount - Decimal.from_float(float(self.amount_paid))
        if self.paid == False and self.amount_paid >= self.total_amount:
            self.paid = True
            self.status = 'paid'

            
        super().save(*args, **kwargs)


    def __str__(self):
        return self.creditor.get_full_name()

    def get_absolute_url(self):
        return reverse('loan-detail', kwargs={'pk': self.pk})

    def get_percentage(self):
        return f"{self.percentage}%"




class AproveCredit(models.Model):
    credit      =   models.ForeignKey(Credit, on_delete=models.PROTECT, related_name='credit')
    sender      =   models.ForeignKey(Profile, on_delete=models.PROTECT)
    recipient   =   models.ForeignKey(User, on_delete=models.PROTECT, related_name="recipient")
    amount      =   models.DecimalField(max_digits=10, decimal_places=2)
    created_on  =   models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=AproveCredit)
def my_receiver(sender, instance, created, **kwargs):
    if created:
        ##Get and update sender
        sender = get_object_or_404(Profile, user=instance.sender.user)
        sender.balance -= instance.amount
        sender.working_capital += instance.amount
        sender.save()
        #Get and update recipient
        #recipient = User.objects.get(id=instance.recipient.id)
        #recipient.main_balance += instance.amount
        #recipient.save()




class PayLoan(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.PROTECT)
    paid_by  =   models.ForeignKey(User, on_delete=models.PROTECT)
    amount  =   models.DecimalField(max_digits=8, decimal_places=2)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.paid_by.get_full_name()} - {self.amount}"


@receiver(post_save, sender=PayLoan)
def payLoanSignal(sender, instance, created, **kwargs):
    if created:
        approver_user = User.objects.get(id=instance.credit.approved_by.user.id)
        obj = Credit.objects.get(id=instance.credit.id)
        credit_approver = Profile.objects.get(user = approver_user)
        obj.amount_paid += instance.amount
        obj.save()
        credit_approver.balance += instance.amount
        credit_approver.working_capital -= instance.amount

        if credit_approver.working_capital <= 0.00:
            credit_approver.working_capital = 0.00

        if obj.amount_paid >= obj.total_amount:
            credit_approver.interest += obj.interest - obj.interest * Decimal.from_float(float(0.08))
            credit_approver.total_interest += obj.interest - obj.interest * Decimal.from_float(float(0.08))
            credit_approver.balance -= obj.interest

            #get witness and add revenue share (8%)
            witness = User.objects.get(id=obj.witness_1.id)
            witness.revenue_share+= obj.interest * Decimal.from_float(float(0.08))
            witness.save()

            ## Create Witnes Revenue Object
            LoanWitnessRevenue.objects.create(
                credit = obj,
                witness = obj.witness_1,
                revenue = obj.interest * Decimal.from_float(float(0.08))
            )


            #get creditor and add witness renue
            creditor = obj.approved_by
            credit_approver.revenue_share += obj.interest * Decimal.from_float(float(0.08))
        


            if credit_approver.working_capital >= 0.01:
                credit_approver.working_capital += Decimal.from_float(float(obj.interest))
            

        credit_approver.save()



'''
class LoanWitnessRequest(models.Model):
    credit  =   models.ForeignKey(Credit, on_delete=models.CASCADE)
    witness =   models.ForeignKey(User, on_delete=models.CASCADE)
    message =   models.CharField(max_length=200)
    approve =   models.BooleanField(default=False)
    created_on  =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.witness
'''


class LoanWitnessRevenue(models.Model):
    credit      =   models.ForeignKey(Credit, on_delete=models.CASCADE)
    witness =   models.ForeignKey(User, on_delete=models.CASCADE)
    revenue =   models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_out    =   models.BooleanField(default=False)
    created_on  =   models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.witness.get_full_name()



'''
    
    message =   models.CharField(max_length=200)  
'''