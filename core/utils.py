import datetime
from appointment.models import DoctorAvailability

def get_doctor_availability(doctor, date):
    # Fetch non-recurring availability
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor, date=date, is_recurring=False
    )

    # Fetch recurring availability
    recurring_availabilities = DoctorAvailability.objects.filter(
        doctor=doctor, is_recurring=True
    )

    # Check if the given date matches any recurring pattern
    day_of_week = date.weekday()
    recurring_slots = []

    for availability in recurring_availabilities:
        pattern = availability.recurring_pattern
        if day_of_week in pattern['days_of_week']:
            recurring_slots.append({
                'start_time': pattern['start_time'],
                'end_time': pattern['end_time']
            })

    return availabilities, recurring_slots

