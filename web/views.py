from server.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.translation import ugettext_lazy as _
import logging
from server.models.random_item import RandomItemResultItem
from server.bom.random_number import RandomNumberDraw

logger = logging.getLogger("echaloasuerte")


# Create your views here.
def index(request):
    logger.info("Serving index page.")
    return render_to_response('index.html', {'request': request}, context_instance=RequestContext(request))


def random_number_draw(request):
    #TODO: proper logging
    #TODO: save draws in db
    #TODO: proper error propagation
    context = {}
    if request.method == 'POST':
        draw_form = RandomNumberDrawForm(request.POST)
        if draw_form.is_valid():
            raw_draw = draw_form.cleaned_data
            bom_draw = RandomNumberDraw(**raw_draw)#This works because form and python object have the same member names
            if bom_draw.is_feasible():
                result = bom_draw.toss()
                res_numbers = result["numbers"]
                context = {'results': res_numbers}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = RandomNumberDrawForm()

    context['draw'] = draw_form
    return render(request, 'random_number.html', context)


def random_item_draw(request):
    context = {}
    if request.method == 'POST':
        draw_form = RandomItemDrawForm(request.POST)
        item_formset = ItemFormSet(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if item_formset.is_valid():
                item_set = item_formset.save()
                for item in item_set:
                    draw.items.add(item)
                if draw.is_feasible():
                    result = draw.toss()
                    context = {'results': result.items.values_list('name', flat=True)}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = RandomItemDrawForm()
        item_formset = ItemFormSet(queryset=Item.objects.none())

    context['draw'] = draw_form
    context['items'] = item_formset
    context['helper'] = ItemFormsetHelper()
    return render(request, 'random_item.html', context)


def coin_draw(request):
    context = {}
    if request.method == 'POST':
        draw_form = CoinDrawForm(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if draw.is_feasible():
                result = draw.toss()
                context = {'result': result.value}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = CoinDrawForm()

    context['draw'] = draw_form
    return render(request, 'coin.html', context)


def dice_draw(request):
    context = {}
    if request.method == 'POST':
        draw_form = DiceDrawForm(request.POST)
        if draw_form.is_valid():
            draw = draw_form.save()
            if draw.is_feasible():
                result = draw.toss()
                list = []
                for number in result.dice.all():
                    list.append(number.value)
                context = {'results': list}
            else:
                print("The draw is not feasible!")
        else:
            print(draw_form.errors)
    else:
        draw_form = DiceDrawForm()

    context['draw'] = draw_form
    return render(request, 'dice.html', context)

def under_construction(request):
    return render(request, 'under_construction.html', {})
