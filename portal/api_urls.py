from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import (
    DepartmentViewSet,
    ClassGroupViewSet,
    TeacherViewSet,
    SubjectViewSet,
    StudentViewSet,
    CourseEnrollmentViewSet,
    AttendanceRecordViewSet,
    FeeStructureViewSet,
    PaymentViewSet,
    ExamViewSet,
    ResultViewSet,
    AnnouncementViewSet,
    MessageViewSet,
    AuditLogViewSet,
    DashboardAPIView,
)

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('classes', ClassGroupViewSet)
router.register('teachers', TeacherViewSet)
router.register('subjects', SubjectViewSet)
router.register('students', StudentViewSet)
router.register('enrollments', CourseEnrollmentViewSet)
router.register('attendance', AttendanceRecordViewSet)
router.register('fees', FeeStructureViewSet)
router.register('payments', PaymentViewSet)
router.register('exams', ExamViewSet)
router.register('results', ResultViewSet)
router.register('announcements', AnnouncementViewSet)
router.register('messages', MessageViewSet)
router.register('audit-logs', AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]
