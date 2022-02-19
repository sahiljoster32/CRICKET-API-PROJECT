from django.shortcuts import render

def homeView(request):
    """This view redirected to home page template!!"""

    return render(request, 'index.html')    