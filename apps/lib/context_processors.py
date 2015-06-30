#from cart.cart import Cart

#from akva.models import Category as akvacategory
#from akva.models import Color, Color2
#from zoo.models import Category as zoocategory
#from terrain.models import Category as terraincategory

from records.models import Visits

from django.contrib.auth.forms import AuthenticationForm


def context_proc(request):
    out = {}

    out['select_date'] = None
    out['visits'] = None
#    request.POST[]



    #out['zoocategory']     = zoocategory.published.all();
    #out['terraincategory'] = terraincategory.published.all();
    
    
    return out

def auth_form(request):
    out = {}
    
    out['auth_form'] = login_form = AuthenticationForm()

    if request.user.is_authenticated():
        out['auth_user'] = request.user
    
    return out