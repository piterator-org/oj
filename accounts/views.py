from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import reverse

from django.contrib import auth

from .forms import UserCreationForm, ErrorList


def index(request):
    raise Http404


def robots_txt(request):
    return HttpResponse('User-agent: *\nDisallow: /login/?\n'
                        'Disallow: /logout/\nDisallow: /switch/\n',
                        'text/plain')


class LoginView(auth.views.LoginView):

    def get_redirect_url(self):
        """Return the user-originating redirect URL."""
        return self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )


class LogoutView(auth.views.LogoutView):

    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            next_page = self.next_page

        if (self.redirect_field_name in self.request.POST
                or self.redirect_field_name in self.request.GET):
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
        return next_page


# def signup_page(request):
#     if request.method == 'POST':
#         context = {}
#         if 'verification' in request.POST:
#             if hashlib.sha1(request.POST['verification'].encode()).hexdigest() == request.POST['sha']:
#                 try:
#                     user = User(username=request.POST['username'], email=request.POST['email'])
#                     user.set_password(request.POST['password'])
#                     user.save()
#                 except IntegrityError:
#                     context['sha'] = request.POST['sha']
#             else:
#                 context['sha'] = request.POST['sha']
#         else:
#             verification = str(random.randrange(100000, 999999))
#             context['sha'] = hashlib.sha1(verification.encode()).hexdigest()
#             send_mail('邮箱验证码', verification, 'Piteator<admin@piterator.com>', [request.POST['email']], fail_silently=False)
#         return render(request, 'accounts/signup.html', context)
#     else:
#         return render(request, 'accounts/email.html')

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, error_class=ErrorList)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
