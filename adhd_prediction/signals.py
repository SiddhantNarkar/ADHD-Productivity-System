from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from datetime import timedelta

from .models import UserLoginStreak


@receiver(user_logged_in)
def update_login_streak(sender, request, user, **kwargs):
    if user.is_superuser:
        return

    today = timezone.now().date()
    streak, created = UserLoginStreak.objects.get_or_create(user=user)

    # First login ever
    if streak.last_login_date is None:
        streak.current_streak = 1
        streak.longest_streak = 1
        streak.longest_streak_start = today
        streak.last_login_date = today
        streak.update_rank()
        streak.save()
        return

    # Already logged in today
    if streak.last_login_date == today:
        return

    # Continuous login
    if streak.last_login_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        # STREAK BROKEN
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
            streak.longest_streak_end = streak.last_login_date

        streak.current_streak = 1
        streak.longest_streak_start = today

    # Update longest streak
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
        streak.longest_streak_start = today
        streak.longest_streak_end = None  # still active

    streak.last_login_date = today
    streak.update_rank()
    streak.save()
