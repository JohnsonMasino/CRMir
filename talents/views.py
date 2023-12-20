from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Talent
from .forms import TalentForm

@login_required
def talent_list(request):
    talents = Talent.objects.all()
    return render(request, 'talent_list.html', {'talents': talents})

@login_required
def talent_create(request):
    if request.method == 'POST':
        form = TalentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Talent created successfully.')  # Add success message
            return redirect('talents:talent_list')
    else:
        form = TalentForm()
    return render(request, 'talent_form.html', {'form': form})

@login_required
def talent_update(request, talent_id):
    talent = get_object_or_404(Talent, pk=talent_id)
    if request.method == 'POST':
        form = TalentForm(request.POST, instance=talent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Talent updated successfully.')  # Add success message
            return redirect('talents:talent_list')
    else:
        form = TalentForm(instance=talent)
    return render(request, 'talent_form.html', {'form': form})

@login_required
def talent_delete(request, talent_id):
    talent = get_object_or_404(Talent, pk=talent_id)
    if request.method == 'POST':
        talent.delete()
        messages.success(request, 'Talent deleted successfully.')  # Add success message
        return redirect('talents:talent_list')
    return render(request, 'talent_confirm_delete.html', {'talent': talent})
