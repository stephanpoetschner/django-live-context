# coding: utf-8
from django.template.context import BaseContext, ContextPopException

class LiveContext(BaseContext):
    """
    Inner-Class, storing context-dictionary and making usage with
    "with"-statement possible.

    depends on django.template.context.BaseContext
    """
    def __init__(self, instance, dict_):
        super(LiveContext, self).__init__(dict_)
        self.target_instance = instance

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.target_instance.unset_live_context()


class LiveContextMixin(object):
    """
    Usage in myapp:
    # myapp/ctx.py
    from live_context.decorators import read_live_context
    from live_context.ctx import LiveContextMixin

    class MyModelLiveContextMixin(LiveContextMixin):

        @read_live_context
        def is_mymodel_visible(self, mymodel_instance, some_more_context=None):
            if some_more_context and mymodel_instance in some_more_context:
                return True
            return False


    # profiles/models.py
    from django.db import models
    from myapp.ctx import MyModelLiveContextMixin

    class UserProfile(models.Model, MyModelLiveContextMixin):
        ...


    # myapp/views.py
    from django.http import Http404

    def some_view(request, mymodel_instance, some_context_value):
        user_profile = request.user.get_profile()

        if not user_profile.is_mymodel_visible(
           some_keyword=some_context_value,
           mymodel_instance=mymodel_instance
        ):
            raise Http404

    or

    def some_view(request, mymodel_instance, some_context_value):
        user_profile = request.user.get_profile()
        with user_profile.set_live_context({
                u'some_more_context': some_context_value,
                u'mymodel_instance': my_model_instance,
            }):
            if not request.user.get_profile.is_mymodel_visible():
                raise Http404
    """

    def set_live_context(self, context={}):

        if not hasattr(self, 'live_context'):
            self.live_context = LiveContext(self, context)
        else:
            d = self.live_context.push()
            d.update(context)

        return self.live_context

    def unset_live_context(self):
        try:
            self.live_context.pop()
        except ContextPopException:
            del self.live_context
