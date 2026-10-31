from django.db.models import Q, Count
from .models import Company
from django.db.models import Sum
from .forms import CompanyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def company_list(request):
    query = request.GET.get('q','').strip()

    companies = Company.objects.annotate(
    deals_count=Count('deals')
)

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

@login_required
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

@login_required
def company_edit(request,company_id):
    company = get_object_or_404(Company, id=company_id)

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


@login_required
def company_detail(request, company_id):
    
    company = get_object_or_404(Company, pk=company_id)

    deals = company.deals.all()

    open_deals = deals.exclude(stage__in=['won', 'lost'])
    won_deals = deals.filter(stage='won')

    context = {
        'company': company,
        'deals': deals,
        'open_deals_count': open_deals.count(),
        'open_deals_value': open_deals.aggregate(
            total=Sum('value')
        )['total'] or 0,
        'won_deals_value': won_deals.aggregate(
            total=Sum('value')
        )['total'] or 0,
    }
    return render(request,'companies/company_detail.html', context)