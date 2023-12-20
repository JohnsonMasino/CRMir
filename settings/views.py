from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from payments.forms import PaymentMethodForm
from payments.models import PaymentMethod
from settings.forms import CompanySettingsForm, RoleForm
from settings.models import CompanySettings, Role


@login_required
def profile_page(request):
    user = request.user  # Get the logged-in user object
    # You can now access user attributes like user.username, user.email, etc.

    context = {
        'user': user,
    }

    return render(request, 'profile_page.html', context)


@login_required
def settings_view(request):
    settings = CompanySettings.objects.first()
    if request.method == 'POST':
        form = CompanySettingsForm(request.POST, instance=settings)
        payment_methods_form = PaymentMethodForm()
        roles_form = RoleForm()

        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('settings:')
        elif payment_methods_form.is_valid():
            payment_methods_form.save()
            messages.success(request, 'Payment method saved')

        else:
            messages.error(request, 'Failed to update settings. Please check the form and try again.')
    else:
        form = CompanySettingsForm(instance=settings)
        payment_methods_form = PaymentMethodForm()
        roles_form = RoleForm()

    return render(request,
                  'settings.html',
                  {
                      'form': form,
                      'payment_methods_form': payment_methods_form,
                      'roles_form': roles_form,
                      'payment_methods': PaymentMethod.objects.all(),
                      'roles': Role.objects.all()
                  })
