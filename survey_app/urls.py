from django.urls import path, include
from .views import survey_form, approve_survey, send_survey_email, user_dashboard,success_page,survey_success,survey_approval_list
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("survey_form/", survey_form, name="survey_form"),
    path("send_survey/", send_survey_email, name="send_survey_email"),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path("success/",success_page, name="success_page"),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("survey_success/", survey_success, name="survey_success"),
    # path('admin/approve/<int:survey_id>/', approve_survey, name='approve_survey'),
    path("surveyresponse/approve/<int:survey_id>/", approve_survey, name="approve_survey"),
    path('survey-approvals/', survey_approval_list, name='survey_approval_list'),

    

]





