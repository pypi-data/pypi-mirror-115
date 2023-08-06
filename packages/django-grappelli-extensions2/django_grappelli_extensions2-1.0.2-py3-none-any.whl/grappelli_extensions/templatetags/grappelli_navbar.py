import sys

from django import template
from django.conf import settings
from classytags.helpers import InclusionTag


def get_extension(setting, default, *args, **kwargs):
    extension = getattr(settings, setting, default)
    parts = extension.split(".")
    module = ".".join(parts[:-1])
    __import__(module)
    module = sys.modules[module]
    return getattr(module, parts[-1])


def get_navbar():
    return get_extension('GRAPPELLI_EXTENSIONS_NAVBAR',
                         'grappelli_extensions.navbar.Navbar')


def has_perms(request, params):
    if 'perm' in params:
        perms = [params['perm']]
    else:
        perms = params.get('perms', [])
    if perms:
        perms = [request.user.has_perm(p) for p in perms]
        return any(perms)
    return True


def get_children(Navbar, request):
    children = []
    for node in Navbar.nodes:
        if node.__class__.__name__.endswith("Node"):
            title, params = node.as_tuple()
        else:
            title, params = node

        if not has_perms(request, params):
            continue

        nodes = params.get("nodes", [])
        url = params.get('url')
        root = {'title': title, 'children': [], 'url': url}
        for node in nodes:
            if node.__class__.__name__.endswith("Node"):
                title, params = node.as_tuple()
            else:
                title, params = node

            url = params.get('url')
            node = {'title': title, 'url': url}
            if has_perms(request, params):
                root['children'].append(node)

        if root['children'] or root['url']:
            children.append(root)
    return children


class GrappelliNavbar(InclusionTag):
    name = 'grappelli_navbar'
    template = 'grappelli/navbar.html'

    def get_context(self, context):
        navbar = get_navbar()
        return {'children': get_children(navbar, context['request'])}


register = template.Library()
register.tag(GrappelliNavbar)
