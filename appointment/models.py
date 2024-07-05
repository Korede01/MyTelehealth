from django.db import models
from doctor.models import Doctor
from patient.models import Patient

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.user.username} - {self.date} from {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    duration = models.IntegerField(default=30)  # Duration in minutes

    def __str__(self):
        return f"Appointment with {self.doctor.username} by {self.patient.username} on {self.date} at {self.time}"

