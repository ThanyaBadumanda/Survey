from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from .models import SurveyResponse
from .forms import SurveyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
import random
import string

# Admin sends survey link via email
def send_survey_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        survey_link = "http://127.0.0.1:8000/survey_form/"
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



# User fills the survey form



@login_required  # Ensure only logged-in users can access this view
def survey_form(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey_response = form.save(commit=False)
            survey_response.user = request.user  # Assign the logged-in user
            survey_response.save()
            return redirect("survey_success")  

    else:
        form = SurveyForm()

    return render(request, "survey_form.html", {"form": form})



import random
import string
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import SurveyResponse

# def generate_random_password():
#     """Generate a secure random 10-character password with letters and digits."""
#     # return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#     print("Approval process started...")  # Debugging Step 1

####added now
def generate_random_password():
    """Generate a secure random 10-character password with letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
######
@login_required
def approve_survey(request, survey_id):
    """Approve a survey response, generate a password, and send login details via email."""
    survey = get_object_or_404(SurveyResponse, id=survey_id)

    if survey.approved:
        messages.warning(request, "This survey is already approved.")
        return redirect(reverse('survey_approval_list'))

    # Mark the survey as approved
    survey.approved = True
    survey.save()
    print(f"Survey {survey.id} approved for user {survey.user.email}")  # Debugging Step 2


    # Generate a random password
    password = generate_random_password()
    print(f"Generated password: {password}")

    # Update and hash the user's password securely
    user = survey.user
    user.set_password(password)  # Django automatically hashes the password
    user.save()
    print("Password saved successfully!")  # Debugging Step 4

    # Send an email with login credentials
    subject = "Survey Approved - Your Login Details"
    message = f"""
    Dear {user.email},

    Your survey submission has been approved!

    Login at: http://127.0.0.1:8000/login/
    Username: {user.email}
    Password: {password}

    Please log in and change your password immediately for security reasons.

    Regards,
    Survey Admin
    """
    try:
        email_sent = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        print(f"Email sent status: {email_sent}")

        if email_sent:
            messages.success(request, f"Survey by {user.email} has been approved. Login details sent.")
            print("Email sent successfully!")  # For debugging 5
        else:
            messages.error(request, f"Failed to send email to {user.email}.")
            print("Email sending failed!")  # For debugging 6
    except Exception as e:
        messages.error(request, f"Error sending email: {str(e)}")
        print(f"Error sending email: {str(e)}")  # For debugging 7
    return redirect(reverse('survey_approval_list'))






# User Dashboard to show expenses analytics
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import SurveyResponse

@login_required
def user_dashboard(request):
    user_surveys = SurveyResponse.objects.filter(email=request.user.email, is_approved=True)
    
    # Calculate analytics
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


# Check if user is admin
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)  # Only allow staff users
def survey_approval_list(request):
    surveys = SurveyResponse.objects.filter(is_approved=False)  # Get unapproved surveys
    return render(request, 'survey_app/survey_approval_list.html', {'surveys': surveys})

@login_required
@user_passes_test(is_admin)
def approve_survey(request, survey_id):
    survey = get_object_or_404(SurveyResponse, id=survey_id)
    survey.is_approved = True
    survey.save()
    messages.success(request, f"Survey by {survey.user.email} has been approved.")
    return redirect('survey_approval_list')

from django.shortcuts import render
from .models import SurveyResponse
def survey_approval_list(request):
    surveys = SurveyResponse.objects.filter(is_approved=False)  # Use 'surveys' instead of 'pending_surveys'
    return render(request, "survey_app/survey_approval_list.html", {"surveys": surveys})




