from django.shortcuts import render,redirect
from .models import Company
from .forms import CompanyForm
def company_list(request):
    companies = Company.objects.all().order_by('-created_at')
    context = {
        'companies':companies
    }
    return render(request, 'companies/company_list.html',context)



def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()

    return render(request, 'companies/company_form.html', {
        'form': form
    })
