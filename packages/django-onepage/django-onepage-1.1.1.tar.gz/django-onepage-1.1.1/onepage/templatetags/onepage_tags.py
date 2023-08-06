from django import template
from .. import gv

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_items(context, *args, **kwargs):
    request = context['request']
    verified_menu_map = {}
    user = request.user

    if user.is_authenticated:
        for key, menu in gv.menu_map.items():
            submenu = []
            indexed_once = False
            for item in menu['submenu']:
                app_label, act, model = item['id'].split('-')

                permitted = user.has_perm(
                    app_label + '.' + act + '_' + model)

                if permitted:
                    if indexed_once:
                        varified_menu_map[key]['submenu'].append(item)
                    else:
                        varified_menu_map[key] = {
                            'id': menu['id'],
                            'title': menu['title'],
                            'submenu': [item]
                        }
                        indexed_once = True
    else:
        print('User not logged in...')

    return verified_menu_map
