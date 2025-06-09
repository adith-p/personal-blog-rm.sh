from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from pathlib import Path

from .utls.serializer import JsonSerializer
from .utls.filesystem import FileSystem
from .utls.custom_decorator import only_me

# Create your views here.


def index(request):
    p = Path(f"{settings.BASE_DIR}/posts")
    post_list = [i for i in p.iterdir() if i.is_file()]

    json_data = JsonSerializer(post_list).serialize()

    return render(
        request, template_name="blog/index.html", context={"json_data": json_data}
    )


@only_me
def add_post(request):
    from datetime import datetime

    if request.method == "POST":
        day = datetime.now().strftime("%B %d, %Y")

        input_json = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "publishing_date": day,
        }
        post_id = FileSystem.add(input_json)
        return redirect("blog:readPost", file_id=post_id)
    return render(request, template_name="blog/add_post.html")


def read_post(request, file_id: str):

    try:
        json_data = JsonSerializer(FileSystem.read(file_id)).serialize()
        print(json_data)
    except Exception as e:
        raise e
    return render(
        request, template_name="blog/article.html", context={"json_data": json_data}
    )


@only_me
def update_post(request, file_id: str):
    if request.method == "POST":

        date = FileSystem.read(file_id)
        if date != None:
            post = JsonSerializer(date).serialize()
        else:
            raise Http404
        input_json = {
            "id": post["file0"]["id"],
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "publishing_date": post["file0"]["publishing_date"],
        }
        FileSystem.update(input_json, file_id)
        return redirect("blog:readPost", file_id=file_id)

    try:
        json_data = JsonSerializer(FileSystem.read(file_id)).serialize()
    except Exception as e:
        raise Http404
    return render(
        request, template_name="blog/edit_post.html", context={"json_data": json_data}
    )


@only_me
def delete_post(request, file_id):
    if FileSystem().remove(file_id):
        messages.success(request, message="post have been deleted")
        return redirect("user_auth:profile")
    messages.error(request, message="could not delete the post")
