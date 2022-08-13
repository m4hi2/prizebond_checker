from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PrizeBondNumberForm


def profile(request):
    current_user = request.user
    return render(request, "prize_checker/profile.html", {"current_user": current_user})


def add_prize_bond_number(request):
    if not request.user.is_authenticated:
        return redirect("account_login", permanent=True)

    if request.method == "POST":
        form = PrizeBondNumberForm(request.POST)
        if form.is_valid():
            return HttpResponse(form.cleaned_data)
        else:
            return redirect(request, "add")

    return render(
        request=request,
        template_name="prize_checker/add_prizebond_numbers.html",
        context={"form": PrizeBondNumberForm()}
    )


def show_prize_results(request):
    pass
