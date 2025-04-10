from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .models import SurveyResponse
from .forms import SurveyForm

import random
import string
import logging

logger = logging.getLogger(__name__)


#  Utility Functions

def generate_random_password():
    """Generate a secure random 10-character password with letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def is_admin(user):
    return user.is_staff


#  Survey Email Sender 

def send_survey_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        survey_link = "http://192.168.1.149:8000/survey_form/"
        send_mail(
            "Complete Your Daily Expense Survey",
            f"Click the link to complete your survey: {survey_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, "Form link sent successfully!")
        return redirect("success_page")
    return render(request, "send_survey_email.html")


def success_page(request):
    return render(request, "success_page.html")


def survey_success(request):
    return render(request, "survey_success.html")


def survey_form(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()  # Email now gets saved with the form
            return redirect("survey_success")
    else:
        form = SurveyForm()

    return render(request, "survey_form.html", {"form": form})



# Survey Approval

@login_required
@user_passes_test(is_admin)
def survey_approval_list(request):
    surveys = SurveyResponse.objects.filter(is_approved=False)
    return render(request, 'survey_app/survey_approval_list.html', {'surveys': surveys})


@login_required
@user_passes_test(is_admin)
def approve_survey(request, survey_id):
    survey = get_object_or_404(SurveyResponse, id=survey_id)

    if survey.is_approved:
        messages.warning(request, "This survey is already approved.")
        return redirect(reverse('survey_approval_list'))

    survey.is_approved = True
    survey.save()
    logger.info(f"✅ Survey {survey.id} approved for email {survey.email}")

    password = generate_random_password()
    logger.info(f"🔑 Generated password for {survey.email}: {password}")

    # ✅ Create or fetch the user account
    user, created = User.objects.get_or_create(
        username=survey.email,
        defaults={"email": survey.email}
    )
    user.set_password(password)
    user.save()

    # ✅ Assign user to survey
    survey.user = user
    survey.save()
    logger.info(f"🔒 Password updated and user assigned for {user.email}")

    subject = "Survey Approved - Your Login Details"
    login_url = "http://192.168.1.149:8000/accounts/login/"
    message = f"""
    Dear {user.email},

    Your survey submission has been approved!

    Login at: {login_url}
    Username: {user.email}
    Password: {password}

    Please log in and change your password immediately for security reasons.

    Regards,
    Survey Admin
    """

    try:
        logger.info(f"📧 Attempting to send email to {user.email}...")
        email_sent = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        if email_sent:
            messages.success(request, f"✅ Survey by {user.email} approved. Login details sent.")
            logger.info(f"✅ Email successfully sent to {user.email}")
        else:
            messages.error(request, f"❌ Failed to send email to {user.email}.")
            logger.error(f"❌ Email sending failed for {user.email}")
    except Exception as e:
        messages.error(request, f"❌ Error sending email: {str(e)}")
        logger.error(f"❌ Error sending email to {user.email}: {e}")

    return redirect(reverse('survey_approval_list'))



# User Dashboard 

@login_required
def user_dashboard(request):
    user_surveys = SurveyResponse.objects.filter(email=request.user.email, is_approved=True)

    total_tea_expense = user_surveys.aggregate(Sum('tea_expense'))['tea_expense__sum'] or 0
    total_coffee_expense = user_surveys.aggregate(Sum('coffee_expense'))['coffee_expense__sum'] or 0
    total_biscuit_expense = user_surveys.aggregate(Sum('biscuit_expense'))['biscuit_expense__sum'] or 0
    total_smoking_expense = user_surveys.aggregate(Sum('smoking_expense'))['smoking_expense__sum'] or 0

    context = {
        'user_surveys': user_surveys,
        'total_tea_expense': total_tea_expense,
        'total_coffee_expense': total_coffee_expense,
        'total_biscuit_expense': total_biscuit_expense,
        'total_smoking_expense': total_smoking_expense,
    }

    return render(request, 'survey_app/user_dashboard.html', context)
