from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = ["tea_expense", "coffee_expense", "biscuit_expense", "smoking_expense"]


