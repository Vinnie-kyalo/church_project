from django.db import models

class Student(models.Model):
    REGISTRATION_YEARS = [
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025'),
    ]

    reg_no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    baptism_status = models.CharField(max_length=50, choices=[('Baptized', 'Baptized'), ('Not Baptized', 'Not Baptized')])
    role_in_church = models.CharField(max_length=100)
    registration_year = models.IntegerField(choices=REGISTRATION_YEARS)

    def __str__(self):
        return f"{self.name} ({self.reg_no})"
