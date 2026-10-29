
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from deals.models import Deal
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    tasks = Task.objects.select_related(
        'contact',
        'deal'
    ).all()

    search_query = request.GET.get('q', '').strip()

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    today = timezone.localdate()

    overdue_tasks = tasks.filter(
        is_completed=False,
        due_date__date__lt=today
    )

    today_tasks = tasks.filter(
        is_completed=False,
        due_date__date=today
    )

    upcoming_tasks = tasks.filter(
        is_completed=False,
        due_date__date__gt=today
    )

    completed_tasks = tasks.filter(
        is_completed=True
    )

    return render(
        request,
        'tasks/task_list.html',
        {
            'overdue_tasks': overdue_tasks,
            'today_tasks': today_tasks,
            'upcoming_tasks': upcoming_tasks,
            'completed_tasks': completed_tasks,
            'search_query': search_query,
        }
    )




@login_required
def task_create(request):
    deal_id = request.GET.get('deal') or request.POST.get('deal')
    deal = None

    if deal_id:
        deal = get_object_or_404(Deal, id=deal_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)

            if deal:
                task.deal = deal

            task.save()
            return redirect('deal_detail', deal_id=deal.id) if deal else redirect('task_list')
    else:
        form = TaskForm(initial={'deal': deal} if deal else None)

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'deal': deal,
        }
    )


@login_required
@require_POST
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.is_completed = not task.is_completed
    task.save(update_fields=['is_completed'])

    return redirect(
        request.META.get('HTTP_REFERER', '/tasks/')
    )

@login_required
@require_POST
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()

    return redirect('task_list')

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'task': task,
        }
    )
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related('contact', 'deal'),
        id=task_id
    )

    return render(
        request,
        'tasks/task_detail.html',
        {'task': task}
    )
