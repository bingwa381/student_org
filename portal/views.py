from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import (
    StudentRegistrationForm,
    StudentProfileForm,
    AssignRegistrationForm,
    AdminStudentCreationForm,
)
from .models import Student

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'portal/home.html')

def signup(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            return render(request, 'portal/registration_success.html', {
                'student': student,
            })
    else:
        form = StudentRegistrationForm()
    return render(request, 'portal/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff:
                login(request, user)
                return redirect('admin_students')
            try:
                student = Student.objects.get(user=user)
                if student.is_approved:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is pending approval.')
            except Student.DoesNotExist:
                messages.error(request, 'Student profile not found.')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'portal/login.html')

@login_required
def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        return render(request, 'portal/dashboard.html', {'student': student})
    except Student.DoesNotExist:
        if request.user.is_staff:
            return redirect('admin_students')
        messages.error(request, 'Student profile not found.')
        return redirect('logout')

@login_required
def edit_profile(request):
    try:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
        else:
            form = StudentProfileForm(instance=student)
        return render(request, 'portal/edit_profile.html', {'form': form, 'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('logout')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def admin_students(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    query = request.GET.get('q', '')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(registration_number__icontains=query) |
            Q(course__icontains=query)
        )
    
    return render(request, 'portal/admin_students.html', {'students': students, 'query': query})

@login_required
def admin_add_student(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = AdminStudentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added and approved successfully.')
            return redirect('admin_students')
    else:
        form = AdminStudentCreationForm()

    return render(request, 'portal/admin_add_student.html', {'form': form})

@login_required
def assign_registration(request, student_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = AssignRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_approved = True
            student.save()
            messages.success(request, f'Registration number assigned and {student} approved.')
            return redirect('admin_students')
    else:
        form = AssignRegistrationForm(instance=student)

    return render(request, 'portal/admin_assign_registration.html', {'form': form, 'student': student})

@login_required
def approve_student(request, student_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    if not student.registration_number:
        messages.error(request, 'Assign a registration number before approving this student.')
        return redirect('assign_registration', student_id=student.id)
    student.is_approved = True
    student.save()
    messages.success(request, f'Student {student} approved.')
    return redirect('admin_students')

@login_required
def delete_student(request, student_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    student.user.delete()  # This will cascade delete the student
    messages.success(request, 'Student deleted.')
    return redirect('admin_students')
