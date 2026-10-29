from django.shortcuts import render
from django.utils import timezone
from companies.models import Company
from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task
from django.db.models import Count,Sum
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_home(request):
    context = {
        'companies_count': Company.objects.count(),
        'contacts_count': Contact.objects.count(),
        'deals_count': Deal.objects.count(),
        'tasks_count': Task.objects.count(),

        'recent_companies': Company.objects.order_by('-created_at')[:5],
        'recent_contacts': Contact.objects.order_by('-created_at')[:5],
        'recent_deals': Deal.objects.order_by('-created_at')[:5],
        'recent_tasks': Task.objects.order_by('-created_at')[:5],
        'deals_by_stage': Deal.objects.values('stage').annotate(total=Count('id'), 
                        total_value=Sum('value')).order_by('stage'),   
         'upcoming_tasks': Task.objects.filter(is_completed=False, due_date__gte=timezone.now()
                        ).order_by('due_date')[:5],

                        'today': timezone.localdate(),
'tomorrow': timezone.localdate() + timedelta(days=1),
          }
    

    return render(request, 'dashboard/dashboard.html', context)