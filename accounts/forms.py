from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join, html_safe

from django.contrib import auth
from django.contrib.auth import password_validation

from captcha.fields import ReCaptchaField


class UsernameField(auth.forms.UsernameField):

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
            'autofocus': True,
            'class': 'form-control',
        }


class ErrorList(forms.utils.ErrorList):

    def __init__(self, initlist=None, error_class=None):
        super().__init__(initlist)

        print(self.error_class)
        if error_class is None:
            self.error_class = 'alert alert-danger'
        else:
            self.error_class = 'errorlist {}'.format(error_class)

    def as_ul(self):
        if not self.data:
            return ''

        return format_html(
            '<ul class="{}">{}</ul>',
            self.error_class,
            format_html_join('', '<li>{}</li>', ((e,) for e in self))
        )


class AuthenticationForm(auth.forms.AuthenticationForm):
    username = UsernameField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control'}),
    )
    captcha = ReCaptchaField()


class UserCreationForm(auth.forms.UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    captcha = ReCaptchaField()

    class Meta(auth.forms.UserCreationForm.Meta):
        field_classes = {'username': UsernameField}
