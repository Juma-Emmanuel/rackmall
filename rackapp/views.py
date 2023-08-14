import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import datetime
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

        # Call push_data to post the data and get the response
        response = push_data(data)

        if response.status_code == 200:
            # Parse the response JSON to get the generated key
            response_data = response.json()
            data_key = response_data.get("name")

            if image:
                image_url = upload_image(image.read(), image.name)
                # Save the image URL in the Realtime Database under the specific data key
                db.reference(f"data/{data_key}").update({"image_url": image_url})

        return redirect("data_list_view")

    return render(request, "post_data.html")





   








def data_list_view(request):
    data = get_data()
    return render(request, "data_list.html", {"data": data})