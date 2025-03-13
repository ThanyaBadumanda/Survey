from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tea_expense = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    coffee_expense = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    biscuit_expense = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    smoking_expense = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Renamed for clarity
    submitted_at = models.DateTimeField(default=now)

    def total_expense(self):
        return self.tea_expense + self.coffee_expense + self.biscuit_expense + self.smoking_expense

    def __str__(self):
        return f"Survey Response ({self.user.username if self.user else 'Anonymous'}) - Approved: {self.is_approved}"

    

 