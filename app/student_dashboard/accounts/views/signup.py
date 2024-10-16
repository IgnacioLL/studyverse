from django.views.generic import View
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model



def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."


    message = render_to_string("accounts/acc_active_email.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str((urlsafe_base64_decode(uidb64)))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your e-mail confirmation")

        return redirect('accounts:signin')
    else:
        messages.error(request, "Activation link invalid!")

    return redirect('index')

class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            activateEmail(request, user, forms.cleaned_data.get('email'))

        context = {"form": forms}
        return render(request, self.template_name, context)