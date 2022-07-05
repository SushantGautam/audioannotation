from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),

    path('user/<int:user_id>/block/', views.UserChangeBlock.as_view(), name='user_block'),
    path('user/<int:user_id>/unblock/', views.UserChangeBlock.as_view(), name='user_unblock'),
]

# Contract_urls
urlpatterns += [
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('contracts/create/', views.ContractCreateView.as_view(), name='contract_create'),
    path('contracts/<int:pk>/', views.ContractDetailView.as_view(), name='contract_detail'),
    path('contracts/<int:pk>/edit/', views.ContractEditView.as_view(), name='contract_edit'),
    path('contracts/<int:pk>/delete/', views.ContractDeleteView.as_view(), name='contract_delete'),
]

# Speaker page URLS
urlpatterns += [
    path('records/speakers/', views.SpeakerListView.as_view(), name='speaker_list'),
    path('records/speakers/<int:pk>/', views.SpeakerDetailView.as_view(), name='speaker_detail'),
    path('records/speakers/<int:pk>/results', views.SpeakerResultView.as_view(), name='speaker_result'),
    path('speaker/<int:user_id>/verify/', views.SpeakerVerification.as_view(), name='speaker_verify'),

    path('records/contracts/', views.SpeakerContractSignList.as_view(), name='speaker_contract'),
    path('records/contracts/<int:contract_id>/verify/', views.SpeakerContractSignVerify.as_view(),
         name='speaker_contract_verify'),
    path('records/speakers/verify-multiple-speakers/', views.verify_multiple_speakers, name='verify_multiple_speakers')
]

# Worker page URLS
urlpatterns += [
    path('tasks/workers/', views.WorkerListView.as_view(), name='worker_list'),
    path('tasks/workers/<int:pk>/', views.WorkerDetailView.as_view(), name='worker_detail'),
    path('worker/<int:user_id>/verify/', views.WorkerVerification.as_view(), name='worker_verify'),

    path('tasks/contracts/', views.WorkerContractSignList.as_view(), name='worker_contract'),
    path('tasks/contracts/<int:contract_id>/verify/', views.WorkerContractSignVerify.as_view(),
         name='worker_contract_verify'),

    path('tasks/allocation/', views.WorkerTaskList.as_view(), name='worker_task_list'),
    path('tasks/<int:task_id>/verify/', views.WorkerTaskVerify.as_view(),
         name='task_verify'),
]

# Management URLS
urlpatterns += [
    path('category-management', views.CategoryManagementListView.as_view(), name='category_management'),
    path('evaluation-management', views.EvaluationManagementListView.as_view(), name='evaluation_management'),

    # Questions
    path('questions/', views.QuestionListPage.as_view(), name='question_list'),
    path('questions/create/', views.QuestionsCreateView.as_view(), name='question_create_ajax'),
    path('questions/<int:pk>/edit/', views.QuestionsUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView, name='question_delete'),
    path('questions/delete_multiple_question/', views.MultipleQuestionDeleteView,
         name='delete_multiple_question'),

    # Question Sets
    path('question_set', views.QuestionSetListView.as_view(), name='question_set_list'),
    path('question_set/create/', views.QuestionSetCreateView.as_view(), name='question_set_create'),
    path('question_set/<int:pk>/edit/', views.QuestionsSetUpdateView.as_view(), name='question_set_update'),
    path('question_set/<int:pk>/delete/', views.QuestionSetDeleteView, name='questionset_delete'),
    path('question_set/delete_multiple/', views.MultipleQuestionSetDeleteView,
         name='delete_multiple_questionset'),

    # ExamsetSubmission
    path('examset/', views.ExamsList.as_view(), name='examset_list'),
    path('examset/<int:pk>/', views.ExamsDetail.as_view(), name='examset_detail'),
    path('exam/<int:exam_id>/submit/', views.submitExam, name='exam_submit'),
    path('examset/submitted/', views.ExamSetSubmissionList.as_view(), name='examset_submission_list'),
    path('examset/<int:examsetsubmission_id>/stt/generate/', views.ExamSetGenerateStt.as_view(),
         name='examset_generate_stt')
]
