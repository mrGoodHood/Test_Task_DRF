from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, ExchangeProposal
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    """Главная со списком всех объявлений."""
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'ads': ads})

@login_required
def create_ad(request):
    """ Создание объявления."""
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
    """ Редактирование объявления."""
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
    """ Удаление объявления."""
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")
    ad.delete()
    return redirect('home')