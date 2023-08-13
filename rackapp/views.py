import firebase_admin
from django.shortcuts import render, redirect
from .firebase_utils import push_data, get_data, upload_image
# Create your views here.
def post_data_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        data = {
            "title": title,
            "description": description,
        }
        push_data(data)
        
        if image:
            upload_image(image.read(), image.name)

        return redirect("data_list_view")

    return render(request, "post_data.html")

def data_list_view(request):
    data = get_data()
    return render(request, "data_list.html", {"data": data})