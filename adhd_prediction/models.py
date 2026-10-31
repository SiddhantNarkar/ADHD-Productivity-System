from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

# Assessment Session Model

class UserAccount(models.Model):
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    complete_address = models.TextField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10)
    password = models.CharField(max_length=300)
    account_type = models.CharField(max_length=50)
    total_points = models.IntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super(UserAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name



class SubGuardian(models.Model):
    guardian = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="sub_guardians")

    subguardian_image = models.ImageField(upload_to='images/', null=True, blank=True)
    subguardian_full_name = models.CharField(max_length=150, null=True, blank=True)
    subguardian_email = models.EmailField(null=True, blank=True)
    subguardian_phone = models.BigIntegerField(null=True, blank=True)
    subguardian_dob = models.DateField(null=True, blank=True)
    subguardian_gender = models.CharField(max_length=20, null=True, blank=True)
    subguardian_occupation = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Sub-Guardian of {self.guardian.full_name}"



class UserLoginStreak(models.Model):
    RANK_CHOICES = [
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
        ("platinum", "Platinum"),
        ("diamond", "Diamond"),
    ]

    # LINK TO YOUR USER MODEL
    user = models.OneToOneField( UserAccount, on_delete=models.CASCADE, related_name="login_streak")

    # CURRENT STREAK
    current_streak = models.PositiveIntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    # LONGEST STREAK
    longest_streak = models.PositiveIntegerField(default=0)
    longest_streak_start = models.DateField(null=True, blank=True)
    longest_streak_end = models.DateField(null=True, blank=True)

    # RANK
    current_rank = models.CharField( max_length=20, choices=RANK_CHOICES, default="bronze")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # RANK LOGIC
    def update_rank(self):
        if self.current_streak >= 50:
            self.current_rank = "diamond"
        elif self.current_streak >= 35:
            self.current_rank = "platinum"
        elif self.current_streak >= 20:
            self.current_rank = "gold"
        elif self.current_streak >= 10:
            self.current_rank = "silver"
        else:
            self.current_rank = "bronze"

    # STREAK UPDATE ON LOGIN
    def update_streak_on_login(self):
        today = timezone.now().date()

        # FIRST LOGIN EVER
        if self.last_login_date is None:
            self.current_streak = 1
            self.longest_streak = 1
            self.longest_streak_start = today
            self.longest_streak_end = None

        # ALREADY LOGGED IN TODAY
        elif self.last_login_date == today:
            return

        # CONTINUOUS LOGIN (YESTERDAY)
        elif self.last_login_date == today - timedelta(days=1):
            self.current_streak += 1

        # STREAK BROKEN
        else:
            if self.current_streak >= self.longest_streak:
                self.longest_streak = self.current_streak
                self.longest_streak_end = self.last_login_date

            self.current_streak = 1
            self.longest_streak_start = today

        # UPDATE LONGEST STREAK IF EXCEEDED
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
            self.longest_streak_start = today
            self.longest_streak_end = None

        # UPDATE META
        self.last_login_date = today
        self.update_rank()
        self.save()

    def __str__(self):
        return f"{self.user.full_name} – {self.current_streak} days"



class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    message = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"



























# test models

from django.db import models
from django.utils import timezone


class AssessmentSession(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('mcq_in_progress', 'MCQ In Progress'),
        ('mcq_completed', 'MCQ Completed'),
        ('game1_in_progress', 'Game 1 In Progress'),
        ('game1_completed', 'Game 1 Completed'),
        ('game2_in_progress', 'Game 2 In Progress'),
        ('completed', 'Completed')
    ]

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    created_date = models.DateField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    age_at_assessment = models.IntegerField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # MCQ timing
    mcq_start_time = models.DateTimeField(null=True, blank=True)
    mcq_end_time = models.DateTimeField(null=True, blank=True)
    selected_language = models.CharField(max_length=50, null=True, blank=True, default="English")

    # Game 1 timing
    game1_start_time = models.DateTimeField(null=True, blank=True)
    game1_end_time = models.DateTimeField(null=True, blank=True)

    # Game 2 timing
    game2_start_time = models.DateTimeField(null=True, blank=True)
    game2_end_time = models.DateTimeField(null=True, blank=True)

    # ML model
    ai_severity_level = models.IntegerField(null=True, blank=True)
    ai_confidence = models.FloatField(null=True, blank=True)
    ai_flag_borderline = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.status}"


class MCQQuestion(models.Model):

    DOMAIN_CHOICES = [
        ("Inattention", "Inattention"),
        ("Hyperactivity", "Hyperactivity"),
        ("Impulsivity", "Impulsivity"),
    ]

    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    language = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)

    domain = models.CharField(
        max_length=50,
        choices=DOMAIN_CHOICES,
        default="Inattention"
    )

    def __str__(self):
        return self.question_text[:50]


class MCQResponse(models.Model):

    session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)

    selected_option = models.CharField(max_length=1)  # A, B, C, D
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.user.full_name} - Q{self.question.id}"


class Game1Result(models.Model):

    session = models.OneToOneField(AssessmentSession, on_delete=models.CASCADE)

    total_stimuli = models.IntegerField(default=0)
    total_targets = models.IntegerField(default=0)

    correct_presses = models.IntegerField(default=0)
    false_presses = models.IntegerField(default=0)
    missed_targets = models.IntegerField(default=0)

    average_reaction_time_ms = models.FloatField(null=True, blank=True)

    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Game1 - {self.session.user.full_name}"


class Game2Result(models.Model):

    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]

    session = models.ForeignKey(
        AssessmentSession,
        on_delete=models.CASCADE,
        related_name="game2_levels"
    )

    level = models.IntegerField(choices=LEVEL_CHOICES)

    correct_sequence = models.JSONField()
    user_sequence = models.JSONField()

    correct_count = models.IntegerField()
    completion_time_seconds = models.FloatField()

    score = models.FloatField()  # raw percentage score per level

    class Meta:
        unique_together = ("session", "level")
        ordering = ["level"]

    def __str__(self):
        return f"{self.session.user.full_name} - Game2 Level {self.level}"



class AssessmentReportHistory(models.Model):

    # RELATIONSHIPS
    user = models.ForeignKey(
        "UserAccount",
        on_delete=models.CASCADE,
        related_name="final_reports"
    )

    session = models.OneToOneField(
        "AssessmentSession",
        on_delete=models.CASCADE,
        related_name="final_report"
    )

    # REPORT META
    report_date = models.DateField(default=timezone.now)
    generated_at = models.DateTimeField(auto_now_add=True)

    report_version = models.CharField(max_length=20, default="v2 1.0")
    scoring_version = models.CharField(max_length=20, default="v2 1.0")
    model_version = models.CharField(max_length=50, default="ml-v2 1.0")

    # PATIENT SNAPSHOT (FROZEN)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    # AI RESULT
    severity_level_number = models.IntegerField()
    severity_label = models.CharField(max_length=50)

    ai_confidence_score = models.FloatField(blank=True, null=True)

    # DOMAIN SCORES (%)
    inattention_pct = models.FloatField()
    hyperactivity_pct = models.FloatField()
    impulsivity_pct = models.FloatField()

    # COGNITIVE METRICS (GAME DATA)
    attention_accuracy = models.FloatField()
    false_press_rate = models.FloatField()
    reaction_time = models.FloatField()

    level1 = models.FloatField()
    level2 = models.FloatField()
    level3 = models.FloatField()

    memory_drop = models.FloatField()
    avg_completion_time = models.FloatField()

    def __str__(self):
        return f"Final Report - {self.session.user.full_name} - Session {self.session.id}"

    class Meta:
        ordering = ["-generated_at"]

class PersonalizedTask(models.Model):
    SESSION_CHOICES = [
        ("morning", "Morning"),
        ("midday", "Midday"),
        ("evening", "Evening"),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ("guardian_account", "Guardian Account"),
        ("personal_account", "Personal Account"),
    ]

    LEVEL_CHOICES = [
        (1, "Mild"),
        (2, "Moderate"),
        (3, "High"),
        (4, "Severe"),
    ]

    day_number = models.IntegerField()  # 1–7
    level = models.IntegerField(choices=LEVEL_CHOICES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)

    task_no = models.IntegerField()
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()

    session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    symptom = models.CharField(max_length=255)

    average_time = models.IntegerField(help_text="Minutes")
    points = models.IntegerField()

    def __str__(self):
        return f"Level {self.level} - Day {self.day_number} - {self.task_title}"


class UserTaskStatus(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey("UserAccount", on_delete=models.CASCADE)
    task = models.ForeignKey(PersonalizedTask, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "task")

    def __str__(self):
        return f"{self.user.full_name} - {self.task.task_title}"


class DailyProgress(models.Model):

    user = models.ForeignKey("UserAccount", on_delete=models.CASCADE)

    day_number = models.IntegerField()
    level = models.IntegerField()

    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    pending_tasks = models.IntegerField(default=0)

    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "day_number", "date")

    def __str__(self):
        return f"{self.user.full_name} - Day {self.day_number}"