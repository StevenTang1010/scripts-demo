from django import forms
from django.core.exceptions import ValidationError


class ResetPwdForm(forms.Form):
    password = forms.CharField(max_length=20, min_length=6)
    repassword = forms.CharField(max_length=20, min_length=6)

    def clean(self):
        cleaned_date = super(ResetPwdForm, self).clean()
        password = cleaned_date.get('password')
        repassword = cleaned_date.get('repassword')

        if password != repassword:
            raise ValidationError('两次密码输入不一致')

        return cleaned_date