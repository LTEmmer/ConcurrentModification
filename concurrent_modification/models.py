# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    acct_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    acct_type = models.CharField(max_length=32)
    is_active = models.IntegerField()
    balance = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounts'


class Addresses(models.Model):
    address_username = models.ForeignKey('PersonalDetails', models.DO_NOTHING, db_column='address_username', blank=True, null=True)
    address_street = models.CharField(max_length=128)
    addr_city = models.CharField(max_length=64)
    addr_state = models.CharField(max_length=32)
    addr_zip = models.CharField(max_length=5)

    class Meta:
        db_table = 'addresses'


class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'admins'


class BankBranches(models.Model):
    bank_id = models.AutoField(primary_key=True)
    location = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'bank_branches'


class DebitCards(models.Model):
    card_number = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    card_account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'debit_cards'


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    employee_bank_branch = models.ForeignKey(BankBranches, models.DO_NOTHING, db_column='employee_bank_branch', blank=True, null=True)

    class Meta:
        db_table = 'employees'


class HelpTickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    ticket_message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'help_tickets'


class Loans(models.Model):
    loan_id = models.AutoField(primary_key=True)
    original_amount = models.FloatField()
    amount_paid = models.FloatField()
    amount_owed = models.FloatField()
    apr = models.FloatField()
    total_interest = models.FloatField()
    paid = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    loan_account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'loans'


class Overdrafts(models.Model):
    overdraft_id = models.AutoField(primary_key=True)
    amount_over = models.FloatField()
    penalty_issued = models.IntegerField()
    paid = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    overdraft_transaction = models.ForeignKey('Transactions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'overdrafts'


class PersonalDetails(models.Model):
    details_username = models.ForeignKey('Users', models.DO_NOTHING, db_column='details_username', to_field='username', blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(unique=True, max_length=128)
    phone_num = models.CharField(unique=True, max_length=12)
    phone_area = models.CharField(max_length=3)

    class Meta:
        db_table = 'personal_details'


class Transactions(models.Model):
    trans_id = models.AutoField(primary_key=True)
    acct = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    trans_type = models.CharField(max_length=64)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_time = models.DateTimeField(blank=True, null=True)
    trans_note = models.CharField(max_length=256, blank=True, null=True)
    trans_amt = models.FloatField()

    class Meta:
        db_table = 'transactions'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=64)
    pwd = models.CharField(unique=True, max_length=64)
    created_at = models.DateTimeField(blank=True, null=True)
    acct = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'users'
