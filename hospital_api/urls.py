from django.urls import path
from .views import DoctorReportAPIView, login
from . import views

urlpatterns = [
    path('login/', login),
    path('doctors/create/',views.create_doctor),# the general manager can create users for doctors 
    path('assisstant/create/',views.create_assistant),# the general manager can create users for assisstant
    path('doctors/',views.DoctorList.as_view(), name='list-doctor'),# the general manager can view all the doctors in the system
    path('doctors/<int:pk>/', views.DoctorDetail.as_view(), name='doctor-detail'),# the general manager can view all details about a doctors 
    path('doctors/<int:pk>/', views.DoctorUpdate.as_view(), name='doctor-update'),# the general manager can update a doctors 
    path('doctors/<int:pk>/', views.DoctorDelete.as_view(), name='doctor-delete'),# the general manager can delete a doctor
    path('assistants/', views.AssistantList.as_view(), name='assistants-list'),# the general manager can view all the assistants in the system and create new ones
    path('assistants/<int:pk>/', views.AssistantDetail.as_view(), name='assistants-detail'),# the general manager can view details about assistants and delete  
    path('patients-manager/', views.PatientLists.as_view(), name='patient-list'),# the general manager can view  all the patients in the system
    path('patients-manager/<int:pk>/', views.PatientDetail.as_view(), name='patient-detail'),# the general manager can view  all the details of a patients in the system
    path('pacients/create/', views.PacientCreate.as_view(), name='patient-create'),# the general manager and doctor cand create patients
    path('patients-manager/<int:pk>/', views.PatientDelete.as_view(), name='patient-delete'),# the general manager can delete patients
    #path('patients2/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    #path('assistants2/', views.AssistantListCreateView.as_view(), name='assistant-list-create'),
    path('assignments/', views.AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('prescription/', views.PrescriptionListCreateView.as_view()),#doctor can make prescription for a patient
    path('patients/apply-treatments/', views.TreatmentAppliedView.as_view()),#the assistent can apply tratment only to the patients she has acces to
    path('patients/doctor/', views.PatientsAssignedToDoctor.as_view()),#after the doctor logs in he has access to all his patients
    path('treatments/<int:pk>/', views.Treatment.as_view()),# the general manager or the doctor can delete or get detail about the treatment
    path('treatments/', views.TreatmentList.as_view()),# the general manager or the doctor can list all the treatments
    path('patients/<int:patient_pk>/treatments/', views.TreatmentAppliedReport.as_view()),# the general manager or the doctor can list a report
    path('doctor-report/', views.DoctorReportAPIView.as_view())#the general manager can list a report
    
]