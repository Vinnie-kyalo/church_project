# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse
from .models import Student
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import os


# Dashboard
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'home/index.html')


# Dynamic pages loader
@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# Cohorts view (with student filtering)
@login_required
def cohorts_view(request):
    cohorts = {
        2022: Student.objects.filter(registration_year=2022),
        2023: Student.objects.filter(registration_year=2023),
        2024: Student.objects.filter(registration_year=2024),
        2025: Student.objects.filter(registration_year=2025),
    }
    return render(request, 'home/cohorts.html', {'cohorts': cohorts})


# Download student list by year as PDF (styled like browser with Times New Roman)
@login_required
def download_students_by_year(request, year):
    students = Student.objects.filter(registration_year=year)

    # Render HTML with students data
    html_string = render_to_string('home/students_pdf_template.html', {
        'students': students,
        'year': year
    })

    # PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="students_{year}.pdf"'

    # Times New Roman font location
    font_path = "/usr/share/fonts/truetype/msttcorefonts/times.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/msttcorefonts/timesnewroman.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/times.ttf"

    css = CSS(string=f'''
        @page {{ size: A4; margin: 1cm }}
        body {{ font-family: "Times New Roman", serif; font-size: 12pt; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }}
        h2 {{
            text-align: center;
        }}
    ''')

    HTML(string=html_string).write_pdf(response, stylesheets=[css])
    return response


# Tithe and Offerings
@login_required
def tithe_offerings_view(request):
    return render(request, 'home/tithe_offerings.html')


# Events and Programs
@login_required
def events_programs_view(request):
    return render(request, 'home/events_programs.html')


# Promotions
@login_required
def promotions_view(request):
    return render(request, 'home/promotions.html')


# Settings
@login_required
def settings_view(request):
    return render(request, 'home/settings.html')
