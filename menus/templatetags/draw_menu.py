
from __future__ import annotations
from typing import Dict, List, Any, Set
from django import template
from menus.models import MenuItem

register = template.Library()

@register.inclusion_tag('menus/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    """
    Рисуем меню по имени. В БД уходим один раз: забираем все пункты меню разом.
    Дальше собираем дерево в памяти и раскрываем только нужные ветки.
    """
    request = context.get('request')

    # 1 запрос
    items = list(
        MenuItem.objects.select_related('parent', 'menu')
        .filter(menu__name=menu_name)
        .order_by('parent__id', 'order', 'title')
    )

    # Быстрый доступ по id
    by_id: Dict[int, MenuItem] = {i.id: i for i in items}
    children: Dict[int | None, List[MenuItem]] = {}
    for it in items:
        children.setdefault(it.parent_id, []).append(it)

    # Предрасчёт ссылок
    url_by_id: Dict[int, str] = {}
    for it in items:
        url_by_id[it.id] = it.get_url()

    # ищем активный пункт
    current_path = getattr(request, 'path', '') or ''
    candidates = [it.id for it in items if url_by_id[it.id] == current_path]

    def depth(iid: int) -> int:
        d = 0
        cur = by_id.get(iid)
        while cur and cur.parent_id:
            d += 1
            cur = by_id.get(cur.parent_id)
        return d

    active_id = max(candidates, key=depth) if candidates else None

    expanded: Set[int] = set()
    if active_id:
        cur = by_id.get(active_id)
        while cur and cur.parent_id:
            expanded.add(cur.parent_id)
            cur = by_id.get(cur.parent_id)
        expanded.add(active_id)

    def build(parent_id: int | None) -> List[dict[str, Any]]:
        nodes: List[dict[str, Any]] = []
        for ch in sorted(children.get(parent_id, []), key=lambda x: (x.order, x.title.lower())):
            node = {
                'id': ch.id,
                'title': ch.title,
                'url': url_by_id[ch.id],
                'children': build(ch.id) if ch.id in expanded else [],
            }
            nodes.append(node)
        return nodes

    tree = build(None)
    return {'menu_name': menu_name, 'nodes': tree, 'active_id': active_id}
