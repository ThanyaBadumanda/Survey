from django.http import HttpResponse

def home_view(request):
    return HttpResponse("🚀 Server is up and running!")
