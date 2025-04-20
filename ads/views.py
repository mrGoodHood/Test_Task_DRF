from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

def home(request):
    """Главная страница."""
    ads_list = Ad.objects.all().order_by('-created_at')
    paginator = Paginator(ads_list, 10)  # 5 объявлений на страницу

    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)

    return render(request, 'home.html', {'ads': ads})

# Объявления
@login_required
def create_ad(request):
    """Создание объявления."""
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('home')
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})

@login_required
def edit_ad(request, ad_id):
    """Редактирование объявления."""
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form})

@login_required
def delete_ad(request, ad_id):
    """Удаление объявления."""
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")
    ad.delete()
    return redirect('home')

def search_ads(request):
    """Поиск и фильтрация объявлений."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')

    ads_list = Ad.objects.all().order_by('-created_at')

    if query:
        ads_list = ads_list.filter(title__icontains=query) | ads_list.filter(description__icontains=query)
    if category:
        ads_list = ads_list.filter(category__icontains=category)
    if condition:
        ads_list = ads_list.filter(condition=condition)

    paginator = Paginator(ads_list, 10)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)

    return render(request, 'ads/search_results.html', {'ads': ads})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


# Предложения обмена
@login_required
def create_proposal(request):
    """Создание предложения обмена."""
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('home')
    else:
        form = ProposalForm()
    return render(request, 'proposals/create_proposal.html', {'form': form})

@login_required
def update_proposal(request, proposal_id):
    """Обновление статуса предложения (только для получателя)."""
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden("Вы не можете изменить статус этого предложения.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(ExchangeProposal.STATUS_CHOICES):
            proposal.status = new_status
            proposal.save()
    return redirect('view_proposals')

@login_required
def view_proposals(request):
    """Просмотр предложений обмена."""
    all_proposals = ExchangeProposal.objects.all().order_by('-created_at')

    if request.GET.get('mine') == 'true':
        all_proposals = all_proposals.filter(
            ad_sender__user=request.user
        ) | all_proposals.filter(
            ad_receiver__user=request.user
        )

    status_filter = request.GET.get('status')
    if status_filter:
        all_proposals = all_proposals.filter(status=status_filter)

    return render(request, 'proposals/view_proposal.html', {
        'proposals': all_proposals,
        'status_filter': status_filter,
        'only_mine': request.GET.get('mine') == 'true'
    })