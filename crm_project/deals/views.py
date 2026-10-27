
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import Deal
from .forms import DealForm
from contacts.models import Contact
import json


def deal_list(request):
    deals = Deal.objects.select_related(
        'company',
        'contact'
    ).all().order_by('-created_at')

    stages = Deal.STAGE_CHOICES

    columns = []

    for stage_code, stage_label in stages:
        stage_deals = deals.filter(stage=stage_code)

        columns.append({
            'code': stage_code,
            'label': stage_label,
            'deals': stage_deals,
            'count': stage_deals.count(),
        })

    context = {
        'deals': deals,
        'columns': columns,
         'stages': stages,
        'open_deals_count': deals.exclude(
            stage__in=['won', 'lost']
        ).count(),
        'won_deals_count': deals.filter(
            stage='won'
        ).count(),
        'lost_deals_count': deals.filter(
            stage='lost'
        ).count(),
    }

    return render(
        request,
        'deals/deal_list.html',
        context
    )

@require_POST
@csrf_protect
def update_deal_stage(request, pk):
    deal = get_object_or_404(Deal, pk=pk)

    try:
        data = json.loads(request.body)
        new_stage = data.get('stage')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'success': False, 'error': 'Invalid request data'},
            status=400
        )

    valid_stages = [stage[0] for stage in Deal.STAGE_CHOICES]

    if new_stage not in valid_stages:
        return JsonResponse(
            {'success': False, 'error': 'Invalid deal stage'},
            status=400
        )

    deal.stage = new_stage
    deal.save(update_fields=['stage', 'updated_at'])

    return JsonResponse({
        'success': True,
        'stage': deal.stage,
        'message': 'Deal stage updated successfully'
    })

def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('deal_list')
    else:
        form = DealForm()

    return render(request, 'deals/deal_form.html', {
    'form': form,
    'contacts': Contact.objects.all(),
})


def deal_edit(request, pk):
    deal = Deal.objects.get(pk=pk)

    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)

        if form.is_valid():
            form.save()
            return redirect('deal_list')
    else:
        form = DealForm(instance=deal)

    return render(request, 'deals/deal_form.html', {
        'form': form,
        'contacts': Contact.objects.all(),
        'deal': deal,
    })

def deal_delete(request, pk):
    deal = Deal.objects.get(pk=pk)

    if request.method == 'POST':
        deal.delete()
        return redirect('deal_list')

    return render(request, 'deals/deal_confirm_delete.html', {
        'deal': deal,
    })
from django.shortcuts import get_object_or_404, render
from .models import Deal


def deal_detail(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.select_related(
            'company',
            'contact',
            'assigned_to',
        ),
        pk=deal_id
    )

    return render(request, 'deals/deal_detail.html', {
        'deal': deal,
    })