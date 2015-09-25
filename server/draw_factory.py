"""File defining a helper function to be able to create forms using its string
 type name
"""
from server.forms.card_form import CardDrawForm
from server.forms.coin_form import CoinDrawForm
from server.forms.dice_form import DiceDrawForm
from server.forms.link_sets_form import LinkSetsDrawForm
from server.forms.random_item_form import RandomItemDrawForm
from server.forms.random_number_form import RandomNumberDrawForm
from server.forms.random_letter_form import RandomLetterDrawForm
from server.forms.tournament_form import TournamentDrawForm
from server.bom import CoinDraw, DiceDraw, CardDraw, RandomNumberDraw, \
    RandomLetterDraw, TournamentDraw, LinkSetsDraw, RandomItemDraw


REGISTRY = {}


class DrawNotRegistered(Exception):
    """Exception when trying to use an unregistered draw"""


def register_draw(draw_name, bom_class, form_class, template_name):
    """Creates the binding for the draw classes

    It binds the human name with the bom and the draw class

    :param draw_name: human name of the draw
    :param bom_class: bom class
    :param form_class: form class
    :param template_name: name of the template to be used to render the draw

    """
    template_path = 'snippets/draws/' + template_name + '.html'
    REGISTRY[draw_name] = {
        'bom': bom_class,
        'form': form_class
    }
    form_class.NAME_IN_URL = draw_name
    form_class.TEMPLATE_PATH = template_path
    form_class.DrawClass = bom_class


register_draw('coin', CoinDraw, CoinDrawForm, 'CoinDraw')
register_draw('dice', DiceDraw, DiceDrawForm, 'DiceDraw')
register_draw('card', CardDraw, CardDrawForm, 'CardDraw')
register_draw('number', RandomNumberDraw, RandomNumberDrawForm, 'RandomNumberDraw')
register_draw('letter', RandomLetterDraw, RandomLetterDrawForm, 'RandomLetterDraw')
register_draw('tournament', TournamentDraw, TournamentDrawForm, 'TournamentDraw')
register_draw('item', RandomItemDraw, RandomItemDrawForm, 'RandomItemDraw')
register_draw('link_sets', LinkSetsDraw, LinkSetsDrawForm, 'LinkSetsDraw')


def get_draw_name(draw_type=None):
    """Computes the draw name given the type name

    :param draw_type:  name of the draw type
    :return: string with the draw name
    """
    for draw_name, values in REGISTRY.items():
        if values["bom"].__name__ == draw_type:
            return draw_name
    else:
        raise DrawNotRegistered()


def create_form(draw_type, draw_data=None, initial=None):
    """Creates the correct type of a form

    :param draw_type: string name of the draw
    :param draw_data: data of the draw to create the form
    :return: Form that inherits from DrawFormBase
    """
    if draw_type not in REGISTRY:
        raise DrawNotRegistered()

    form_class = REGISTRY[draw_type]["form"]
    if draw_data:
        form = form_class(draw_data)
    else:
        if initial:
            form = form_class(initial=initial)
        else:
            form = form_class()
    return form


def create_draw(draw_type, draw_data=None):
    """Creates a draw

    :param draw_type: string name of the draw
    :param draw_data: data to initialize the draw
    :return: a draw with a type than inherits from DrawBase
    :rtype: BaseDraw
    """
    if draw_type not in REGISTRY:
        raise DrawNotRegistered()

    bom_class = REGISTRY[draw_type]["bom"]
    if draw_data:
        return bom_class(**draw_data)
    else:
        return bom_class()
