# coding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import send_mail
from datetime import datetime
from int.myAuth.forms import UserCreationCustomForm,\
    AuthenticationCustomForm
from int.myAuth.utils.generate_username import generate_username
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login_get(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    form = AuthenticationCustomForm()
    context = RequestContext(request, {'form': form, })

    return render_to_response('myAuth/login.html', context)


@csrf_protect
def login_post(request):
    from django.contrib.auth.views import login
    return login(request, template_name='myAuth/login.html',
                 authentication_form=AuthenticationCustomForm)


def logout_then_login(request):
    if request.user.is_authenticated():
        from django.contrib.auth.views import logout_then_login
        return logout_then_login(request)

    return HttpResponseRedirect('/')


def create_account_success(request, pk):
    user = get_object_or_404(User, pk=pk)

    context = RequestContext(request, {'account': user})
    return render_to_response('myAuth/create_account_success.html', context)


@csrf_protect
def create_account_get(request):
    form = UserCreationCustomForm()
    context = RequestContext(request, {'form': form, })

    return render_to_response('myAuth/create_account.html', context)


@csrf_protect
def create_account_post(request):
    form = UserCreationCustomForm(request.POST)

    if not form.is_valid():
        context = RequestContext(request, {'form': form, })
        return render_to_response('myAuth/create_account.html', context)

    user = form.save()

    context = Context({'account': user})
    template = get_template('myAuth/confirm_account_email.html')
    template = template.render(context)

    send_confirmation_email(template, "ivens@visionetecnologia.com,br",
                            [user.email])

    return HttpResponseRedirect(reverse('myAuth:create_account_success',
                                        args=[user.pk]))


def send_confirmation_email(template, from_, to):
    send_mail("Pague o aluguel!", template, from_, to)


def confirm_account(request, code):
    """ Returns
    1: Account confirmed
    2: Code does not exist
    3: Code has expired"""

    result = 1

    try:
        user = User.objects.get(username=code)

        profile = user.get_profile()
        current_datetime = datetime.now()

        if current_datetime > profile.confirmation_code_expiration_datetime:
            result = 3

        if (result):
            user.is_active = True
            user.username = generate_username(user.email)
            user.save()

    except User.DoesNotExist:
        result = 2

    context = RequestContext(request, {'result': result, 'code': code})
    return render_to_response('myAuth/confirm_account.html', context)


def send_confirmation_code(request, code):
    """ Needs to make a nice html response... maybe someday when I
    actually use this app, I'll do it """
    try:
        user = User.objects.get(username=code)
    except User.DoesNotExist:
        context = RequestContext(request, {'result': 2, 'code': code})
        return render_to_response('myAuth/confirm_account.html', context)

    username = generate_username(user.email)

    user.username = username
    user.save()

    context = Context({'account': user})
    template = get_template('myAuth/confirm_account_email.html')
    template = template.render(context)

    send_confirmation_email(template, "email@email.com",
                            [user.email])

    return render_to_response('myAuth/send_confirmation_code.html',
                              RequestContext(request))
