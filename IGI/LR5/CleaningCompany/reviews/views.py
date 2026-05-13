from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def reviews(request):
    all_review = Review.objects.all()
    return render(request, 'reviews/reviews.html', {'reviews': all_review})

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form})