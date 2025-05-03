# concurrent_modification/admin.py
from django.contrib import admin
from django.utils.html import format_html

from concurrent_modification.models import (
    Users, Accounts, Addresses, Admins, BankBranches,
    DebitCards, Employees, HelpTickets, Loans, Overdrafts,
    PersonalDetails, Transactions
)

#────────── Inline helpers ──────────#
class TransactionInline(admin.TabularInline):
    model           = Transactions
    extra           = 0
    readonly_fields = ("trans_date", "trans_type", "trans_amt", "note_excerpt")
    fields          = ("trans_date", "trans_type", "trans_amt", "note_excerpt")

    def note_excerpt(self, obj):
        return (obj.trans_note[:40] + "…") if obj.trans_note else ""
    note_excerpt.short_description = "Note"

#────────── Users ──────────#
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display   = ("user_id", "username", "email", "is_active", "created_at")
    search_fields  = ("username", "email")
    list_filter    = ("is_active",)
    date_hierarchy = "created_at"
    ordering       = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

#────────── Accounts + inline ledger ──────────#
@admin.register(Accounts)
class AccountAdmin(admin.ModelAdmin):
    list_display   = ("acct_id", "linked_user", "acct_type",
                      "balance_fmt", "is_active", "created_at")
    list_filter    = ("acct_type", "is_active")
    search_fields  = ("acct_id", "user__username")
    inlines        = (TransactionInline,)
    readonly_fields = ("created_at", "updated_at")

    def linked_user(self, obj):
        url = f"/admin/concurrent_modification/users/{obj.user_id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    linked_user.short_description = "User"

    def balance_fmt(self, obj):
        return f"${obj.balance:,.2f}"
    balance_fmt.short_description  = "Balance"
    balance_fmt.admin_order_field  = "balance"

#────────── Transactions ──────────#
@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display   = ("trans_id", "acct", "trans_type",
                      "trans_amt", "trans_date", "short_note")
    search_fields  = ("acct__acct_id", "acct__user__username", "trans_note")
    list_filter    = ("trans_type", "trans_date")
    date_hierarchy = "trans_date"
    readonly_fields = ("created_at",)

    def short_note(self, obj):
        return (obj.trans_note[:50] + "…") if obj.trans_note else ""
    short_note.short_description = "Note"

#────────── Lean config for the rest ──────────#
@admin.register(Addresses)
class AddressAdmin(admin.ModelAdmin):
    list_display  = ("addr_id", "user", "city", "state", "country", "zip_code")
    search_fields = ("user__username", "city", "state", "country", "zip_code")

@admin.register(Admins)
class AdminStaffAdmin(admin.ModelAdmin):
    list_display  = ("admin_id", "user", "role")
    search_fields = ("user__username",)

@admin.register(BankBranches)
class BranchAdmin(admin.ModelAdmin):
    list_display  = ("branch_id", "name", "city", "state")
    search_fields = ("name", "city", "state")

@admin.register(DebitCards)
class DebitCardAdmin(admin.ModelAdmin):
    list_display  = ("card_id", "acct", "masked_num", "is_active", "expiry")
    list_filter   = ("is_active",)
    search_fields = ("card_id", "acct__acct_id", "acct__user__username")

    def masked_num(self, obj):
        return "•••• " + str(obj.card_number)[-4:]
    masked_num.short_description = "Card"

@admin.register(Employees)
class EmployeeAdmin(admin.ModelAdmin):
    list_display  = ("emp_id", "first_name", "last_name", "branch", "role")
    list_filter   = ("role", "branch")
    search_fields = ("first_name", "last_name", "emp_id")

@admin.register(HelpTickets)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ("ticket_id", "user", "subject", "status", "opened_at")
    list_filter   = ("status", "opened_at")
    search_fields = ("subject", "description", "user__username")
    date_hierarchy = "opened_at"

@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    list_display  = ("loan_id", "user", "loan_type", "principal", "status")
    list_filter   = ("loan_type", "status")
    search_fields = ("loan_id", "user__username")

@admin.register(Overdrafts)
class OverdraftAdmin(admin.ModelAdmin):
    list_display  = ("od_id", "acct", "limit_amt", "is_active")
    list_filter   = ("is_active",)
    search_fields = ("od_id", "acct__acct_id", "acct__user__username")

@admin.register(PersonalDetails)
class PersonalAdmin(admin.ModelAdmin):
    list_display  = ("person_id", "user", "phone", "dob")
    search_fields = ("user__username", "phone")

# Optional branding
admin.site.site_header  = "Concurrent Bank — Admin"
admin.site.index_title  = "Concurrent Bank dashboard"
