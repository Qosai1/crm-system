
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone


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




def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(
        request,
        'tasks/task_form.html',
        {'form': form}
    )


@require_POST
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.is_completed = not task.is_completed
    task.save(update_fields=['is_completed'])

    return redirect(
        request.META.get('HTTP_REFERER', '/tasks/')
    )


@require_POST
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()

    return redirect('task_list')


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
