# どのサイトでも同じ内容になるのでコピペで使える
# 検索した際のページネーション　?query=django&page=2の形にしてくれる

from django import template

register = template.Library()

@register.simple_tag
def replace(request, key, vlaue):
    url_dict = request.GET.copy()
    url_dict[key] = vlaue

    return url_dict.urlencode()