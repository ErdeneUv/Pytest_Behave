from tests.utilities.api_utilities import build_a_link_no_login
from behave import when

@when(u'user sends supported brand "{url}" with affiliate params to build link')
def step_impl(context, url):
    is_short = False
    context.url = url
    context.res = build_a_link_no_login(context.url, is_short)
