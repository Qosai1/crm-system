from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from deals.models import Deal
from tasks.models import Task
from django.contrib.auth.decorators import login_required

@login_required
def contact_list(request):

    query = request.GET.get('q','').strip()
    contacts = Contact.objects.select_related('company').all()

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(company__name__icontains=query) |
            Q(job_title__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    contacts = contacts.order_by('-created_at')
    context = {
        'contacts':contacts,
        'query':query,
    }

    return render(request,'contacts/contact_list.html',context)

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact_form.html', {
        'form': form,
    })

@login_required
def contact_edit(request, contact_id):
    contact = Contact.objects.get(id=contact_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'contact': contact,
    })



@login_required
def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')

    return redirect('contact_list')


@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    deals = Deal.objects.filter(contact=contact)

    open_deals = deals.exclude(stage__in=['won', 'lost'])
    won_deals = deals.filter(stage='won')

    tasks = Task.objects.filter(contact=contact)
    open_tasks = tasks.filter(is_completed=False)
    completed_tasks = tasks.filter(is_completed=True)

    context = {
        'contact': contact,
        'deals': deals,
        'open_deals_count': open_deals.count(),
        'open_deals_value': (
            open_deals.aggregate(total=Sum('value'))['total'] or 0
        ),
        'won_deals_value': (
            won_deals.aggregate(total=Sum('value'))['total'] or 0
        ),
        'tasks': tasks,
        'open_tasks_count': open_tasks.count(),
        'completed_tasks_count': completed_tasks.count(),
    }

    return render(
        request,
        'contacts/contact_detail.html',
        context
    )
