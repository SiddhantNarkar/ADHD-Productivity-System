from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_view, name='home_view_urls'),
    path('contact_us/', contact_us_view, name='contact_us_urls'),
    path('about_us/', about_us_view, name='about_us_urls'),
    path('login/', login_view, name='login_view_urls'),
    path('account_type/', account_type_view, name='account_type_view_urls'),
    path('adhd_productivity_module/', adhd_productivity_module_view, name='adhd_productivity_module_view_urls'),
    path('create_guardian_account/', create_guardian_account_view, name='create_guardian_account_view_urls'),
    path('create_personal_account/', create_personal_account_view, name='create_personal_account_view_urls'),

    path('portal_home/', portal_home_view, name='portal_home_view_urls'),
    path('logout/', portal_logout_view, name='portal_logout_view_urls'),
    path('portal_about_us/', portal_about_us_view, name='portal_about_us_view'),
    path('portal_contact_us/', portal_contact_us_view, name='portal_contact_us_view_urls'),
    path('user_account/', portal_user_account_view, name='portal_user_account_view_urls'),
    path('user_account/change_password/', change_password_view, name='change_password_view_urls'),
    path('user_account/delete_account/', delete_account_view, name='delete_account_view_urls'),
    path('user_account/edit_profile/', edit_profile_view, name='edit_profile_view_urls'),
    path('assessment_test/', adhd_assessment_test_view, name='adhd_assessment_test_view_urls'),
    path('personalized_plan/', adhd_personalized_plan_view, name='adhd_personalized_plan_view_view_urls'),
    path("update-task-status/", update_task_status, name="update_task_status"),

    path("api/chat/", chat_api, name="chat_api"),
    path("api/chat/clear/", clear_chat_memory, name="clear_chat_memory"),

    path('instructions/', assessment_landing_page_view, name='assessment_landing_page_view_urls'),
    path('progress/', progress_page_view, name='progress_page_view_urls'),
    path('mcq/', mcq_test_view, name='mcq_test_view_urls'),
    path('gamified_test/', gamified_test_view, name='gamified_test_view_urls'),
    path('report/', report_page_view, name='report_page_view_urls'),
    path('user/report/<int:session_id>/',user_page_assessment_report_view, name="user_page_assessment_report_view_url"),

    path("save-answer/", save_mcq_answer, name="save_mcq_answer"),
    path("submit-mcq/", submit_mcq, name="submit_mcq"),

    path("submit-game1/", submit_game1, name="submit_game1"),
    path("submit-game2/", submit_game2, name="submit_game2"),
    path('finalize_assessment/', finalize_assessment, name='finalize_assessment'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)