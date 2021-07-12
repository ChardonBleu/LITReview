from django.shortcuts import render


# Create your views here.
def log_in(request):
    """
    Arguments:
        request {[type]} -- [description]
    """
    # instructs
    return render(request, 'library/log_in.html', {})


def register(request):
    """
    Arguments:
        request {[type]} -- [description]
    """
    # instructs
    return render(request, 'library/register.html', {})
