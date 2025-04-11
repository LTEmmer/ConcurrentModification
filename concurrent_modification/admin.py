from django.contrib import admin

from concurrent_modification.models import Users, Accounts, Addresses, Admins, BankBranches, DebitCards, Employees, HelpTickets, Loans, Overdrafts, PersonalDetails, Transactions

admin.site.register(Users)
admin.site.register(Accounts)
admin.site.register(Addresses)
admin.site.register(Admins)
admin.site.register(BankBranches)
admin.site.register(DebitCards)
admin.site.register(Employees)
admin.site.register(HelpTickets)
admin.site.register(Loans)
admin.site.register(Overdrafts)
admin.site.register(PersonalDetails)
admin.site.register(Transactions)