from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Company
from .forms import CompanyForm
from django.shortcuts import render, redirect, get_object_or_404



def company_list(request):
    query = request.GET.get('q','').strip()

    companies = Company.objects.all()

    if query:
        companies = companies.filter(
            Q(name__icontains=query)|
            Q(industry__icontains=query)|
            Q(city__icontains=query)|
            Q(phone__icontains=query)|
            Q(email__icontains=query)
        )

    companies = companies.order_by('-created_at')

    context = {
            'companies': companies,
            'query': query,
        }

    return render(request,'companies/company_list.html',context)

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


def company_edit(request,company_id):
    company = Company.objects.get(id=company_id)

    if request.method == 'POST':
        form = CompanyForm(request.POST,instance=company)

        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)

    return render(request,'companies/company_form.html',{
        'form':form,
        'company':company,
    })   



def company_delete(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        company.delete()
        return redirect('company_list')

    return render(request, 'companies/company_confirm_delete.html', {
        'company': company,
    })



def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    context = {
        'company': company,
    }

    return render(request,'companies/company_detail.html', context)