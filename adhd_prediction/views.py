import json
import requests
import random
import numpy as np
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from datetime import date, timedelta
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from .models import MCQQuestion, MCQResponse, AssessmentSession
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .ml_support.feature_builder import build_features
from .ml_support.predictor import predict_severity

#Befour Login Views
def home_view(request):
    template_name = 'adhd_prediction/home.html'

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        message = request.POST.get("message")
        contact_us = ContactMessage(name=name, email=email, contact_number=contact_number, message=message)
        contact_us.save()

    context = {}
    return render(request, template_name, context)



def contact_us_view(request):
    template_name = 'adhd_prediction/contact_us.html'

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        message = request.POST.get("message")
        contact_us = ContactMessage(name=name, email=email, contact_number=contact_number, message=message)
        contact_us.save()

    context = {}
    return render(request, template_name, context )



def about_us_view(request):
    template_name = 'adhd_prediction/about_us.html'
    context = {}
    return render(request, template_name, context )



def account_type_view(request):
    template_name = 'adhd_prediction/account_type.html'
    context = {}
    return render(request, template_name, context )



def adhd_productivity_module_view(request):
    template_name = 'adhd_prediction/adhd_productivity_module.html'
    context = {}
    return render(request, template_name, context )

from django.dispatch import receiver

def login_view(request):
    template_name = 'adhd_prediction/login.html'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserAccount.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id

                # try to get streak if not exists then created
                streak, created = UserLoginStreak.objects.get_or_create(user=user)

                # update login streak
                streak.update_streak_on_login()

                return redirect('portal_home_view_urls')

            else:
                messages.error(request, "Your password is incorrect.")
                return redirect('login_view_urls')

        except UserAccount.DoesNotExist:
            messages.error(request, "Your email id is incorrect.")
            return redirect('login_view_urls')

    return render(request, template_name)



def create_personal_account_view(request):
    template_name = 'adhd_prediction/create_personal_account.html'

    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        complete_address = request.POST.get('complete_address')
        state = request.POST.get('state')
        country = request.POST.get('country') or 'India'
        blood_group = request.POST.get('blood_group')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        account_type = request.POST.get('account_type')

        personal_account = UserAccount(full_name=full_name, email=email, phone=phone, dob=dob, gender=gender, occupation=occupation, complete_address=complete_address, state=state, country=country, blood_group=blood_group, password=password, profile_image=profile_image, account_type=account_type)
        personal_account.save()
        return redirect('login_view_urls')

    context = {}
    return render(request, template_name, context)



def create_guardian_account_view(request):
    template_name = 'adhd_prediction/create_guardian_account.html'

    if request.method == 'POST':
        # MAIN GUARDIAN FIELDS
        profile_image = request.FILES.get('profile_image')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        complete_address = request.POST.get('complete_address')
        state = request.POST.get('state')
        country = request.POST.get('country') or 'India'
        blood_group = request.POST.get('blood_group')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type')

        guardian = UserAccount(full_name=full_name, email=email, phone=phone, dob=dob, gender=gender, occupation=occupation, complete_address=complete_address, state=state, country=country, blood_group=blood_group, password=password, profile_image=profile_image, account_type=account_type)
        guardian.save()

        # ---------- SAVE SUB-GUARDIANS ----------
        subguardian_names = request.POST.getlist('subguardian_full_name')
        subguardian_emails = request.POST.getlist('subguardian_email')
        subguardian_phones = request.POST.getlist('subguardian_phone')
        subguardian_dobs = request.POST.getlist('subguardian_dob')
        subguardian_genders = request.POST.getlist('subguardian_gender')
        subguardian_occupations = request.POST.getlist('subguardian_occupation')
        subguardian_images = request.FILES.getlist('subguardian_image')

        for i in range(len(subguardian_names)):
            name = subguardian_names[i].strip()

            if name == "":
                continue

            image = subguardian_images[i] if i < len(subguardian_images) else None

            SubGuardian.objects.create(guardian=guardian, subguardian_full_name=subguardian_names[i], subguardian_email=subguardian_emails[i], subguardian_phone=subguardian_phones[i], subguardian_dob=subguardian_dobs[i], subguardian_gender=subguardian_genders[i], subguardian_occupation=subguardian_occupations[i], subguardian_image=image )

        return redirect('login_view_urls')

    context = {}
    return render(request, template_name, context)



#After Login Views
def portal_home_view(request):
    template_name = 'adhd_prediction_portal/home.html'

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        message = request.POST.get("message")
        contact_us = ContactMessage(name=name, email=email, contact_number=contact_number, message=message)
        contact_us.save()

    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
            context = {'user': user}
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    return render(request, template_name, context)



def portal_logout_view(request):
    request.session.flush()
    return redirect('home_view_urls')



def portal_about_us_view(request):
    template_name = 'adhd_prediction_portal/about_us.html'

    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
            context = {'user': user}
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    return render(request, template_name, context)



def portal_contact_us_view(request):
    template_name = 'adhd_prediction_portal/contact_us.html'

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        message = request.POST.get("message")
        contact_us = ContactMessage(name=name, email=email, contact_number=contact_number, message=message)
        contact_us.save()

    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
            context = {'user': user}
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    return render(request, template_name, context)



def portal_user_account_view(request):
    template_name = 'adhd_prediction_portal/user_account.html'

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('home_view_urls')

    try:
        user = UserAccount.objects.get(id=user_id)
        streak = user.login_streak
    except UserAccount.DoesNotExist:
        return redirect('home_view_urls')

    # Fetch latest 3 reports
    recent_reports = AssessmentReportHistory.objects.filter(
        user=user
    )[:3]

    total_points = user.total_points or 0

    # Rank thresholds (POINT BASED)
    rank_thresholds = {
        "bronze": 1,
        "silver": 100,
        "gold": 250,
        "platinum": 400,
        "diamond": 650,
    }

    # Determine Rank
    if total_points >= 650:
        rank = "diamond"
        current_min = 650
        next_min = None
    elif total_points >= 400:
        rank = "platinum"
        current_min = 400
        next_min = 650
    elif total_points >= 250:
        rank = "gold"
        current_min = 250
        next_min = 400
    elif total_points >= 100:
        rank = "silver"
        current_min = 100
        next_min = 250
    elif total_points >= 1:
        rank = "bronze"
        current_min = 1
        next_min = 100
    else:
        rank = "bronze"
        current_min = 0
        next_min = 100

    # Progress Calculation
    if next_min:
        progress_percent = int(
            ((total_points - current_min) / (next_min - current_min)) * 100
        )
    else:
        progress_percent = 100

    # Capitalized version for display
    rank_display = rank.capitalize()

    # Rank thresholds
    streak_limits = {"bronze": 1, "silver": 10, "gold": 20, "platinum": 35, "diamond": 50, }

    streak_current_limit = streak_limits.get(streak.current_rank, 1)
    streak_progress_percent = min(int((streak.current_streak / streak_current_limit) * 100), 100)

    context = {
        'user': user,
        'rank': rank,
        'rank_display': rank_display,
        'progress_percent': progress_percent,
        'recent_reports': recent_reports,

        'streak': streak,
        'streak_progress_percent': streak_progress_percent
    }

    return render(request, template_name, context)



def change_password_view(request):
    template_name = 'adhd_prediction_portal/change_password.html'

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('home_view_urls')

    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist:
        return redirect('home_view_urls')

    if request.method == 'POST':
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        # Check old password
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password_view_urls')

        # Check new & confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password_view_urls')

        # Prevent same password reuse
        if check_password(new_password, user.password):
            messages.error(request, 'New password cannot be the same as the old password.')
            return redirect('change_password_view_urls')

        # Basic password length validation
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('change_password_view_urls')

        # Save new password (hashed)
        user.password = make_password(new_password)
        user.save(update_fields=['password'])

        messages.success(request, 'Your password has been updated successfully.')
        return redirect('change_password_view_urls')

    context = {'user': user}
    return render(request, template_name, context)



def delete_account_view(request):
    template_name = 'adhd_prediction_portal/delete_account.html'

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home_view_urls')

    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist:
        return redirect('home_view_urls')

    if request.method == 'POST':
        confirm_password = request.POST.get('confirm_password')

        # Validate password
        if not check_password(confirm_password, user.password):
            messages.error(request, 'Incorrect password. Account not deleted.')
            return redirect('delete_account_view_urls')

        # Delete user
        user.delete()

        # Clear session
        request.session.flush()
        return redirect('home_view_urls')

    context = {'user': user}
    return render(request, template_name, context)



def edit_profile_view(request):
    template_name = 'adhd_prediction_portal/edit_profile.html'

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home_view_urls')

    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist:
        return redirect('home_view_urls')

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.phone = request.POST.get('phone')
        user.dob = request.POST.get('dob')
        user.gender = request.POST.get('gender')
        user.occupation = request.POST.get('occupation')
        user.complete_address = request.POST.get('complete_address')
        user.state = request.POST.get('state')
        user.country = request.POST.get('country')
        user.blood_group = request.POST.get('blood_group')

        # Profile image (only if uploaded)
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')

        user.save()

        return redirect('portal_user_account_view_urls')

    context = {'user': user}
    return render(request, template_name, context)



def adhd_assessment_test_view(request):
    template_name = 'adhd_prediction_portal/adhd_assessment_test.html'

    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
            context = {'user': user}
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    return render(request, template_name, context)



def adhd_personalized_plan_view(request):
    template_name = "assessment_test/personalized_plan.html"
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login_view")

    user = get_object_or_404(UserAccount, id=user_id)

    latest_report = AssessmentReportHistory.objects.filter(
        user=user
    ).first()

    if not latest_report:
        return redirect("adhd_assessment_test_view_urls")

    # Extract report data safely
    last_test_date = latest_report.report_date
    adhd_level_number = int(latest_report.severity_level_number)
    adhd_level_label = latest_report.severity_label

    days_passed = (date.today() - last_test_date).days
    remaining_days = max(0, 7 - days_passed)

    # 7-DAY AUTO RESET LOGIC
    if remaining_days == 0:

        UserTaskStatus.objects.filter(user=user).update(
            status="pending",
            completed_at=None
        )

        DailyProgress.objects.filter(user=user).delete()

        user.total_points = 0
        user.save()

        messages.warning(
            request,
            "Your 7-day personalized plan is completed. Please go through the assessment test again."
        )

        return redirect("adhd_assessment_test_view_urls")

    # Calculate current day safely (1–7)
    current_day = min(days_passed + 1, 7)

    # Normalize account_type (CRITICAL FIX)
    if user.account_type == "Personal Account":
        normalized_account_type = "personal_account"
    elif user.account_type == "Guardian Account":
        normalized_account_type = "guardian_account"
    else:
        normalized_account_type = user.account_type

    # Fetch today's tasks
    tasks = PersonalizedTask.objects.filter(
        level=adhd_level_number,
        account_type=normalized_account_type,
        day_number=current_day
    )

    # Ensure UserTaskStatus exists
    for task in tasks:
        UserTaskStatus.objects.get_or_create(
            user=user,
            task=task
        )

    user_tasks = UserTaskStatus.objects.filter(
        user=user,
        task__in=tasks
    ).select_related("task")

    total_tasks = user_tasks.count()
    completed_count = user_tasks.filter(status="completed").count()
    pending_count = total_tasks - completed_count

    today = date.today()

    # Update daily progress (FIXED VERSION)
    DailyProgress.objects.update_or_create(
        user=user,
        day_number=current_day,
        date=today,
        defaults={
            "level": adhd_level_number,
            "total_tasks": total_tasks,
            "completed_tasks": completed_count,
            "pending_tasks": pending_count,
        }
    )

    context = {
        "user": user,
        "last_test_date": last_test_date,
        "adhd_level_number": adhd_level_number,
        "adhd_level_label": adhd_level_label,
        "remaining_days": remaining_days,
        "total_points": user.total_points,
        "tasks": user_tasks,
        "completed_count": completed_count,
        "pending_count": pending_count,
        "total_tasks": total_tasks,
    }

    return render(request, template_name, context)



def update_task_status(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        status = request.POST.get("status")

        user_task = get_object_or_404(UserTaskStatus, id=task_id)
        user = user_task.user

        if status == "completed":
            if user_task.status != "completed":
                user_task.status = "completed"
                user_task.completed_at = timezone.now()
                user_task.save()

                user.total_points += user_task.task.points
                user.save()

        else:
            if user_task.status == "completed":
                user_task.status = "pending"
                user_task.completed_at = None
                user_task.save()

                user.total_points -= user_task.task.points
                user.save()

        return JsonResponse({
            "success": True,
            "total_points": user.total_points
        })

    return JsonResponse({"success": False})













#ai chat-bots code start from here

# CONFIG
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"   # change only if you downloaded another model
MAX_MEMORY_MESSAGES = 5  # keep memory short & fast

# ADHD Keyword Logic
def keyword_response(message):
    msg = message.lower()

    focus_keywords = ["can't focus", "cannot focus", "distracted", "losing focus"]
    overwhelm_keywords = ["overwhelmed", "too much", "burned out"]
    procrastination_keywords = ["procrastinate", "procrastination", "putting off"]

    if any(k in msg for k in focus_keywords):
        return "Yeah, focus can disappear fast 😅 Want to try a 5-minute reset?"

    if any(k in msg for k in overwhelm_keywords):
        return "That sounds heavy. Let’s slow it down — just one small step."

    if any(k in msg for k in procrastination_keywords):
        return "Totally relatable. Want help making the task feel less annoying?"

    return None


# OPTIMIZED OLLAMA AI RESPONSE
def ollama_response(message, chat_memory):
    """
    Fast + memory-aware local AI
    """

    # Optimized system prompt (SHORT & STRICT)
    system_prompt = (
        "You are a chill ADHD productivity assistant.\n"
        "Reply in 1–3 short sentences.\n"
        "Be friendly, calm, and non-judgmental.\n"
        "No long explanations.\n"
    )

    # Build conversation context (memory)
    context = system_prompt + "\n"

    for turn in chat_memory:
        context += f"User: {turn['user']}\n"
        context += f"Assistant: {turn['bot']}\n"

    context += f"User: {message}\nAssistant:"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": context,
        "stream": False,
        "options": {
            "temperature": 0.6,
            "num_predict": 120
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        reply = response.json().get("response", "").strip()

        if not reply:
            return "I’m thinking… try saying that again 😅"

        # Safety trim
        if len(reply) > 400:
            reply = reply[:400] + "…"

        return reply

    except requests.exceptions.ConnectionError:
        return "I can’t reach my local brain 😅 Is Ollama running?"

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return "My brain glitched for a sec 😅 Try again?"


# CHAT API WITH BASIC MEMORY
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Hey 🙂 I’m listening."})

        # Get session memory
        chat_memory = request.session.get("chat_memory", [])

        # Keyword logic first
        reply = keyword_response(message)

        # AI fallback (with memory)
        if reply is None:
            reply = ollama_response(message, chat_memory)

        # Update memory (keep it short)
        chat_memory.append({
            "user": message,
            "bot": reply
        })

        chat_memory = chat_memory[-MAX_MEMORY_MESSAGES:]

        request.session["chat_memory"] = chat_memory

        return JsonResponse({"reply": reply})

    except Exception as e:
        print("CHAT API ERROR:", e)
        return JsonResponse({
            "reply": "Something went weird 😅 Try again?"
        })


def clear_chat_memory(request):
    request.session.pop("chat_memory", None)
    return JsonResponse({"status": "cleared"})























def assessment_landing_page_view(request):
    template_name = 'assessment_test/assessment_landing_page.html'

    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    if request.method == "POST":

        if not can_start_new_assessment(user):
            messages.error(request, "You can retake assessment after 7 days.")
            return redirect('portal_home_view_urls')

        age = calculate_age(user.dob)

        session = AssessmentSession.objects.create(
            user=user,
            age_at_assessment=age,
            started_at=timezone.now(),
            status='pending'
        )

        request.session['assessment_session_id'] = session.id

        return redirect('progress_page_view_urls')

    return render(request, template_name, {'user': user})



def progress_page_view(request):
    template_name = 'assessment_test/progress_page.html'

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return redirect('home_view_urls')

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    part1_status = ""
    part2_status = ""
    action_url = None
    action_text = None

    # STATUS LOGIC
    if session.status in ["pending", "mcq_in_progress"]:
        part1_status = "Ready to Start" if session.status == "pending" else "In Progress"
        part2_status = "Locked"
        action_url = "mcq_test_view_urls"
        action_text = "Continue to Part 1: MCQ Assessment"

    elif session.status == "mcq_completed":
        part1_status = "Completed"
        part2_status = "Ready to Start"
        action_url = "gamified_test_view_urls"
        action_text = "Continue to Part 2: Gamified Assessment"

    elif session.status == "game1_in_progress":
        part1_status = "Completed"
        part2_status = "In Progress"
        action_url = "gamified_test_view_urls"
        action_text = "Continue to Part 2: Gamified Assessment"

    elif session.status == "completed":
        part1_status = "Completed"
        part2_status = "Completed"
        action_url = "report_page_view_urls"
        action_text = "View Report"

    return render(request, template_name, {
        "user": user,
        "part1_status": part1_status,
        "part2_status": part2_status,
        "action_url": action_url,
        "action_text": action_text
    })



def mcq_test_view(request):

    template_name = 'assessment_test/mcq_test.html'

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return redirect('assessment_landing_page_view_urls')

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    # Guard status
    if session.status not in ["pending", "mcq_in_progress"]:
        return redirect("progress_page_view_urls")

    # First entry
    if session.status == "pending":
        session.status = "mcq_in_progress"
        session.mcq_start_time = timezone.now()
        session.save()

    # Language handling
    selected_language = request.GET.get("language")

    if selected_language:
        session.selected_language = selected_language
        session.save()
    else:
        selected_language = session.selected_language

    questions_queryset = []
    questions_json = []
    answered_ids = []
    answer_map = {}

    if selected_language:
        questions_queryset = MCQQuestion.objects.filter(
            language=selected_language,
            account_type=user.account_type
        ).order_by("id")

        responses = MCQResponse.objects.filter(session=session)

        answered_ids = list(
            responses.values_list("question_id", flat=True)
        )

        for r in responses:
            answer_map[r.question_id] = r.selected_option

        questions_json = list(
            questions_queryset.values(
                "id",
                "question_text",
                "option_a",
                "option_b",
                "option_c",
                "option_d"
            )
        )

    return render(request, template_name, {
        "user": user,
        "questions_queryset": questions_queryset,
        "questions_json": json.dumps(questions_json, cls=DjangoJSONEncoder),
        "selected_language": selected_language,
        "answered_ids": answered_ids,
        "answer_map_json": json.dumps(answer_map)
    })



def gamified_test_view(request):
    template_name = 'assessment_test/gamified_test.html'

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return redirect('home_view_urls')

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status not in [
        "mcq_completed",
        "game1_in_progress",
        "game1_completed",
        "game2_in_progress"
    ]:
        return redirect("progress_page_view_urls")

    show_game1 = False
    show_game2 = False

    # Enter Game 1 first time
    if session.status == "mcq_completed":
        session.status = "game1_in_progress"
        session.game1_start_time = timezone.now()
        session.save()

    # Game 1 Active
    if session.status == "game1_in_progress":
        show_game1 = True

    # After Game 1 completed → prepare Game 2
    elif session.status == "game1_completed":
        session.status = "game2_in_progress"
        session.game2_start_time = timezone.now()
        session.save()
        show_game2 = True

    # Game 2 Active
    elif session.status == "game2_in_progress":
        show_game2 = True

    context = {
        "user": user,
        "session": session,
        "show_game1": show_game1,
        "show_game2": show_game2,
    }

    return render(request, template_name, context)

''' 
# Original view of report_page
def report_page_view(request):
    template_name = 'assessment_test/report_page.html'

    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserAccount.objects.get(id=user_id)
            context = {'user': user}
        except UserAccount.DoesNotExist:
            return redirect('home_view_urls')
    else:
        return redirect('home_view_urls')

    return render(request, template_name, context)
'''
























# assessment supporting logic views

def calculate_age(dob):

    if not dob:
        return 0

    today = timezone.localdate()

    years_difference = today.year - dob.year

    has_had_birthday = (
        (today.month, today.day) >= (dob.month, dob.day)
    )

    if not has_had_birthday:
        years_difference -= 1

    return years_difference



def can_start_new_assessment(user):
    '''
    last_session = AssessmentSession.objects.filter(
        user=user
    ).order_by('-created_date').first()

    if not last_session:
        return True

    if last_session.status != 'completed':
        return False

    if timezone.now().date() >= last_session.created_date + timedelta(days=7):
        return True

    return False
    '''
    return True



@require_POST
def save_mcq_answer(request):

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status != "mcq_in_progress":
        return JsonResponse({"error": "Invalid state"}, status=403)

    question_id = request.POST.get("question_id")
    selected_option = request.POST.get("selected_option")

    question = get_object_or_404(MCQQuestion, id=question_id)

    MCQResponse.objects.update_or_create(
        session=session,
        question=question,
        defaults={"selected_option": selected_option}
    )

    total_questions = MCQQuestion.objects.filter(
        language=session.selected_language,
        account_type=user.account_type
    ).count()

    answered_count = MCQResponse.objects.filter(
        session=session
    ).count()

    return JsonResponse({
        "answered_count": answered_count,
        "total_questions": total_questions
    })




@require_POST
def submit_mcq(request):

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status != "mcq_in_progress":
        return JsonResponse({"error": "Invalid state"}, status=403)

    total_questions = MCQQuestion.objects.filter(
        language=session.selected_language,
        account_type=user.account_type
    ).count()

    answered_count = MCQResponse.objects.filter(
        session=session
    ).count()

    if answered_count != total_questions:
        return JsonResponse({"error": "Incomplete"}, status=400)

    session.status = "mcq_completed"
    session.mcq_end_time = timezone.now()
    session.save()

    return JsonResponse({
        "redirect_url": reverse("progress_page_view_urls")
    })



@require_POST
def submit_game1(request):

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status != "game1_in_progress":
        return JsonResponse({"error": "Invalid state"}, status=403)

    total_stimuli = int(request.POST.get("total_stimuli"))
    total_targets = int(request.POST.get("total_targets"))
    correct_presses = int(request.POST.get("correct_presses"))
    false_presses = int(request.POST.get("false_presses"))
    missed_targets = int(request.POST.get("missed_targets"))
    avg_reaction_time = float(request.POST.get("avg_reaction_time"))

    # Calculate score
    accuracy = (correct_presses / total_targets) * 100 if total_targets > 0 else 0
    penalty = false_presses * 2
    score = max(0, accuracy - penalty)

    Game1Result.objects.create(
        session=session,
        total_stimuli=total_stimuli,
        total_targets=total_targets,
        correct_presses=correct_presses,
        false_presses=false_presses,
        missed_targets=missed_targets,
        average_reaction_time_ms=avg_reaction_time,
        score=score
    )

    session.status = "game1_completed"
    session.game1_end_time = timezone.now()
    session.save()

    return JsonResponse({"success": True})



@require_POST
def submit_game2(request):

    user_id = request.session.get('user_id')
    session_id = request.session.get('assessment_session_id')

    if not user_id or not session_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status != "game2_in_progress":
        return JsonResponse({"error": "Invalid state"}, status=403)

    try:
        user_sequence = json.loads(request.POST.get("user_sequence"))
    except:
        return JsonResponse({"error": "Invalid sequence"}, status=400)

    completion_time = float(request.POST.get("completion_time", 0))
    level = int(request.POST.get("level", 1))

    correct_pattern = json.loads(request.POST.get("correct_pattern", "[]"))

    correct_count = sum(
        1 for i in range(len(correct_pattern))
        if i < len(user_sequence) and user_sequence[i] == correct_pattern[i]
    )

    score = (correct_count / len(correct_pattern)) * 100 if correct_pattern else 0

    Game2Result.objects.update_or_create(
        session=session,
        level=level,
        defaults={
            "correct_sequence": correct_pattern,
            "user_sequence": user_sequence,
            "correct_count": correct_count,
            "completion_time_seconds": completion_time,
            "score": score,
        }
    )

    return JsonResponse({"success": True})



from django.views.decorators.http import require_POST

@require_POST
def finalize_assessment(request):

    user_id = request.session.get("user_id")
    session_id = request.session.get("assessment_session_id")

    if not user_id or not session_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(
        AssessmentSession,
        id=session_id,
        user=user
    )

    # Ensure correct workflow state
    if session.status != "game2_in_progress":
        return JsonResponse({"error": "Invalid state"}, status=403)

    # Ensure exactly 3 Game2 levels completed
    level_count = Game2Result.objects.filter(session=session).count()
    if level_count != 3:
        return JsonResponse({"error": "Incomplete Game 2"}, status=400)

    # Ensure Game1 exists (important for ML)
    if not hasattr(session, "game1result"):
        return JsonResponse({"error": "Game 1 result missing"}, status=400)

    try:
        with transaction.atomic():

            # ----------------------------
            # FINALIZE SESSION TIMING
            # ----------------------------
            now_time = timezone.now()

            session.status = "completed"
            session.game2_end_time = now_time
            session.completed_at = now_time

            features = build_features(session)

            print("Feature length:", len(features[0]))
            print("Features:", features)

            # ----------------------------
            # ML PREDICTION
            # ----------------------------
            features = build_features(session)
            result = predict_severity(features)

            session.ai_severity_level = result["severity_level"]
            session.ai_confidence = result["confidence"]

            if result["confidence"] < 0.60:
                session.ai_flag_borderline = True
            else:
                session.ai_flag_borderline = False

            session.save()


    except Exception as e:

        return JsonResponse(

            {"error": str(e)},

            status=500

        )

    # Clear temporary session memory
    request.session.pop("memory_pattern", None)

    return JsonResponse({
        "redirect_url": reverse("report_page_view_urls")
    })



































#templory added report page code and view

def report_page_view(request):
    template_name = "assessment_test/report_page.html"

    user_id = request.session.get("user_id")
    session_id = request.session.get("assessment_session_id")

    if not user_id or not session_id:
        return redirect("home_view_urls")

    user = get_object_or_404(UserAccount, id=user_id)
    session = get_object_or_404(AssessmentSession, id=session_id, user=user)

    if session.status != "completed":
        return redirect("progress_page_view_urls")

    # ============================
    # FETCH DATA
    # ============================

    game1 = get_object_or_404(Game1Result, session=session)
    game2_levels = Game2Result.objects.filter(session=session).order_by("level")
    mcq_responses = MCQResponse.objects.filter(session=session)

    # ============================
    # DOMAIN CALCULATION
    # ============================

    domain_scores = {
        "Inattention": [],
        "Hyperactivity": [],
        "Impulsivity": []
    }

    score_map = {"A": 0, "B": 1, "C": 2, "D": 3}

    for response in mcq_responses.select_related("question"):
        domain = response.question.domain
        score = score_map.get(response.selected_option, 0)
        if domain in domain_scores:
            domain_scores[domain].append(score)

    def calculate_percent(scores):
        if not scores:
            return 0
        return round((sum(scores) / (len(scores) * 3)) * 100, 2)

    inattention_pct = calculate_percent(domain_scores["Inattention"])
    hyperactivity_pct = calculate_percent(domain_scores["Hyperactivity"])
    impulsivity_pct = calculate_percent(domain_scores["Impulsivity"])

    # ============================
    # GAME 1 METRICS
    # ============================

    attention_accuracy = round(game1.score, 2)

    false_press_rate = (
        round((game1.false_presses / game1.total_stimuli) * 100, 2)
        if game1.total_stimuli > 0 else 0
    )

    reaction_time = round(game1.average_reaction_time_ms or 0, 2)

    # ============================
    # GAME 2 METRICS
    # ============================

    level_scores = {lvl.level: lvl.score for lvl in game2_levels}

    level1 = level_scores.get(1, 0)
    level2 = level_scores.get(2, 0)
    level3 = level_scores.get(3, 0)

    memory_drop = round(level1 - level3, 2)

    avg_completion_time = round(
        np.mean([lvl.completion_time_seconds for lvl in game2_levels]),
        2
    )

    # ============================
    # AI METADATA
    # ============================

    severity_label_map = {
        0: "No ADHD Traits",
        1: "Mild",
        2: "Moderate",
        3: "High",
        4: "Severe"
    }

    severity_label = severity_label_map.get(session.ai_severity_level, "Unknown")


    # SAVE FINAL REPORT (IF NOT EXISTS)
    report_obj, created = AssessmentReportHistory.objects.get_or_create(
        session=session,
        defaults={
            "user": user,
            "report_date": timezone.now().date(),

            # Patient Snapshot
            "phone": user.phone,
            "email": user.email,
            "address": user.complete_address,
            "blood_group": user.blood_group,
            "gender": user.gender,

            # AI
            "severity_level_number": session.ai_severity_level,
            "severity_label": severity_label,

            # Domain Scores
            "inattention_pct": inattention_pct,
            "hyperactivity_pct": hyperactivity_pct,
            "impulsivity_pct": impulsivity_pct,

            # Cognitive Metrics
            "attention_accuracy": attention_accuracy,
            "false_press_rate": false_press_rate,
            "reaction_time": reaction_time,
            "level1": level1,
            "level2": level2,
            "level3": level3,
            "memory_drop": memory_drop,
            "avg_completion_time": avg_completion_time,
        }
    )

    context = {
        "user": user,
        "session": session,
        "report_date": timezone.now().date(),

        # Patient Info
        "phone": user.phone,
        "email": user.email,
        "address": user.complete_address,
        "blood_group": user.blood_group,
        "gender": user.gender,

        # AI
        "severity_level_number": session.ai_severity_level,
        "severity_label": severity_label,

        # Domain Scores
        "inattention_pct": inattention_pct,
        "hyperactivity_pct": hyperactivity_pct,
        "impulsivity_pct": impulsivity_pct,

        # Cognitive Metrics
        "attention_accuracy": attention_accuracy,
        "false_press_rate": false_press_rate,
        "reaction_time": reaction_time,
        "level1": level1,
        "level2": level2,
        "level3": level3,
        "memory_drop": memory_drop,
        "avg_completion_time": avg_completion_time,
    }

    return render(request, template_name, context)



def user_page_assessment_report_view(request,session_id):
    template_name= "assessment_test/user_page_assessment_report.html"

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("home_view_urls")

    user = get_object_or_404(UserAccount, id=user_id)

    report = get_object_or_404(
        AssessmentReportHistory,
        session__id=session_id,
        user=user
    )

    session = report.session

    context = {
        "user": user,
        "session": session,

        "gender": report.gender,
        "blood_group": report.blood_group,
        "phone": report.phone,
        "email": report.email,
        "report_date": report.report_date,

        "severity_level_number": report.severity_level_number,
        "severity_label": report.severity_label,

        "inattention_pct": report.inattention_pct,
        "hyperactivity_pct": report.hyperactivity_pct,
        "impulsivity_pct": report.impulsivity_pct,

        "attention_accuracy": report.attention_accuracy,
        "false_press_rate": report.false_press_rate,
        "reaction_time": report.reaction_time,
        "memory_drop": report.memory_drop,
        "avg_completion_time": report.avg_completion_time,
    }

    return render(request, template_name, context)