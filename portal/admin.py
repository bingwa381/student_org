from django.contrib import admin
from .models import (
    Profile,
    Department,
    ClassGroup,
    Subject,
    Teacher,
    Student,
    StudentDocument,
    CourseEnrollment,
    AttendanceRecord,
    FeeStructure,
    Payment,
    Exam,
    Result,
    Announcement,
    Message,
    AuditLog,
    Event,
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'phone')
    search_fields = ('user__username', 'user__email')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'year')
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'department', 'teacher')
    search_fields = ('title', 'code')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone', 'is_active')
    search_fields = ('user__username', 'user__email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'registration_number', 'department', 'class_group', 'status', 'is_approved')
    search_fields = ('student_id', 'registration_number', 'user__first_name', 'user__last_name')
    list_filter = ('status', 'year_of_study', 'is_approved')

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'document_type', 'uploaded_at')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrolled_at', 'status')
    search_fields = ('student__student_id', 'subject__title')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'recorded_by')

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('department', 'semester', 'amount')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'paid_at')
    search_fields = ('reference',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'schedule_date', 'total_marks')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'grade', 'published')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_public')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'sent_at', 'is_read')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
