from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import SurveyResponse
from .views import approve_survey, survey_approval_list
from django.urls import reverse

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_email", 
        "tea_expense", 
        "coffee_expense", 
        "biscuit_expense", 
        "smoking_expense", 
        "is_approved", 
        "submitted_at",
        "approve_action"
    )
    list_filter = ("is_approved",)
    actions = ["approve_surveys"]

    def get_user_email(self, obj):
        return obj.email or (obj.user.email if obj.user else "Anonymous")
    get_user_email.short_description = "User Email"

    def approve_action(self, obj):
        """Adds an 'Approve' link in the admin panel if the survey is not approved."""
        if not obj.is_approved:
           approve_url = reverse("approve_survey", args=[obj.id])  # Reverse URL mapping
           return format_html('<a href="{}">Approve</a>', approve_url)
        return "Approved"
    approve_action.short_description = "Action"



    def get_urls(self):
        """Adds a custom URL for approving surveys inside the Django Admin panel."""
        urls = super().get_urls()
        custom_urls = [
            path("surveyresponse/approve/<int:survey_id>/", self.admin_site.admin_view(approve_survey), name="approve_survey"),
            path("approvals/", self.admin_site.admin_view(survey_approval_list), name="survey_approval_list"),
        ]
        return custom_urls + urls

    def approve_surveys(self, request, queryset):
        """Bulk approve selected surveys and send login details."""
        for survey in queryset:
            if not survey.is_approved:
                approve_survey(request, survey.id)
    approve_surveys.short_description = "Approve selected surveys & send password"
