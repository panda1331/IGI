from django.shortcuts import render
from vacancies.models import Vacancy

def vacancies(request):
    all_vacancies = Vacancy.objects.all()
    return render(request, "vacancies/vacancies.html", {"vacancies": all_vacancies})