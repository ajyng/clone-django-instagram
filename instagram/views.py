from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from .models import Tag

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() # DB가 먼저 저장이 되어야 한다. manytomany 관계는 pk가 필요하기 때문.

            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect("/") #TODO: get_absolute_url 활용
    else:
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })