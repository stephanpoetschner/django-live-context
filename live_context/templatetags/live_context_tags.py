# coding: utf-8
from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiKeywordArgument

register = template.Library()


class LiveContextTag(Tag):
    """
    {% live_context request.user.get_profile group=group %}
        {{ some_secret_content }}
    {% end_live_context %}
    """
    name = 'live_context'
    options = Options(
        Argument('live_instance'),
        MultiKeywordArgument('live_context', required=False),
        blocks=[('end_live_context', 'nodelist')],
    )

    def render_tag(self, context, live_instance, live_context, nodelist):

        context.push()
        with live_instance.set_live_context(live_context):
            output = nodelist.render(context)

        context.pop()

        return output

register.tag(LiveContextTag)
