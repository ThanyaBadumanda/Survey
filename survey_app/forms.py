from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = SurveyResponse
        fields = ["email","tea_expense", "coffee_expense", "biscuit_expense", "smoking_expense"]


