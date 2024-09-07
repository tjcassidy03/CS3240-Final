from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.contrib import messages


from .UserType import UserType
from django.http import HttpResponseForbidden
from .models import Report

# Create your views here.

from users.forms import ReportForm, UploadFileForm, AdminCommentForm
from users.models import Report, ReportFile


def is_site_admin(user):
    return user.groups.filter(name='Site Admin').exists()


def home(request):
    is_site_admin = request.user.groups.filter(name='SiteAdmin').exists()
    return render(request, "users/home.html", {'is_site_admin': is_site_admin})


def logout_view(request):
    logout(request)
    return redirect("/")


def file_report(request):
    max_size = 50 * 1024 * 1024  # 50 MB in bytes
    if request.method == 'POST':
        form = ReportForm(request.POST, user=request.user)
        files=request.FILES.getlist('document')
        if form.is_valid():

            if files: #check file type/size
                for file in files:
                    if not file.name.endswith(('.txt', '.pdf', '.jpg')):
                        return render(request, f'users/report/file.html', {'form': form, 'fileTypeError': True, 'fileSizeError': False})
                    if file.size > max_size:
                        return render(request, f'users/report/file.html', {'form': form, 'fileTypeError': False, 'fileSizeError': True})

            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.name_of_reporter = request.user.get_full_name()
                report.email_of_reporter = request.user.email
            report.save()

            if files:
                for file in files:
                    originalFileName = file.name
                    newFileName = f'{report.id}{originalFileName}'  # The name format will be the report ID + the original name
                    file.name = newFileName
                    ReportFile.objects.create(report=report, file=file)
            form.save_m2m()
            return redirect(reverse('users:report_submitted', kwargs={'reportID': report.id}))
        else:
            print(form.errors)
    else:
        form = ReportForm(user=request.user)
    return render(request, 'users/report/file.html', {'form': form})


def report_submitted(request, reportID):
    if request.method == 'POST':
        form=UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            reportFile = form.save(commit=False)
            reportFile.report = Report.objects.filter(id=reportID).first()
            uploadedFile = request.FILES["document"]
            reportFile.file = uploadedFile

            originalFileName = uploadedFile.name
            newFileName = f'{reportID}{originalFileName}' #The name format will be the report ID + the original name
            reportFile.file.name = newFileName

            reportFile.save()
            return render(request, f'users/report/submitted.html', {'fileName': originalFileName}) #Show customer the original file name
            #return redirect(reverse('users:report_submitted', kwargs={'reportID': reportID}))
        else:
            print(form.errors)
    else:
        form = UploadFileForm()
    return render(request, f'users/report/submitted.html')


def handle_uploaded_file(f):
    with open("uploads/"+f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
@user_passes_test(is_site_admin, login_url=reverse_lazy('users:home'))
def admin_reports(request):
    reports_to_update = Report.objects.filter(status='new')
    for report in reports_to_update:
        report.status = 'in progress'
        report.save(update_fields=['status'])

    # Handling admin comments
    if 'admin_comment' in request.POST:
        comment_form = AdminCommentForm(request.POST)
        if comment_form.is_valid():
            report_id = request.POST.get('report_id')
            report = get_object_or_404(Report, id=report_id)
            report.admin_comment = comment_form.cleaned_data['admin_comment']
            report.save()
        else:
            pass

    # Handling status updates
    if 'new_status' in request.POST:
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('new_status')
        report = get_object_or_404(Report, id=report_id)
        report.status = new_status
        report.save()

    # Get all reports
    reports = Report.objects.all().order_by('-created_at')
    forms = {report.id: AdminCommentForm(instance=report) for report in reports}
    return render(request, 'users/admin_reports.html', {'reports': reports, 'forms': forms})


@login_required
def user_reports(request):
    user_email = request.user.email
    reports = Report.objects.all().filter(email_of_reporter=user_email).order_by('-created_at')
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        report = get_object_or_404(Report, pk=report_id, email_of_reporter=user_email)
        if report.status == 'new':
            description = request.POST.get('description_of_event', '')
            if description:
                report.description_of_event = description
                report.save()
            else:
                return redirect('users:user_reports')
        else:
            return redirect('users:user_reports')
    return render(request, 'users/user_reports.html', {'reports': reports})



def retract_report(request, report_id):
    try:
        user_email = request.user.email
        report = Report.objects.get(pk=report_id, email_of_reporter=user_email)
        if report.status == 'new':
            report.delete()
            messages.success(request, "Your report has succesfully been retracted.")
        else:
            messages.error(request, 'You can only retract reports with the status "new".')
    except Report.DoesNotExist:
        messages.error(request, 'Report not found.')
    # return render(request, 'users/user_reports.html')
    return redirect('users:user_reports')
