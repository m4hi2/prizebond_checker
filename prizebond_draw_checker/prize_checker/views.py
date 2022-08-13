from django.shortcuts import render, redirect


def profile(request):
    current_user = request.user
    return render(request, "prize_checker/profile.html", {"current_user": current_user})


def add_prize_bond_number(request):
    if not request.user.is_authenticated:
        return redirect("account_login", permanent=True)

    return render(
        request=request,
        template_name="prize_checker/add_prizebond_numbers.html",
        context={"current_user": request.user}
    )


def show_prize_results(request):
    pass
