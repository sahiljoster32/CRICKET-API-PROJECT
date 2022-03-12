from django.shortcuts import render

# This application contains only one page(Home page).
def homeView(request):
    """This view redirected to home page template!!"""

    return render(request, 'index.html')    