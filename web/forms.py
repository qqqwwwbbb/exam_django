from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import User, Application, Category


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                                         message='Разрешены только кириллические '
                                                                                 'буквы, дефис и пробелы')],
                                 error_messages={'required': 'Обязательное поле'})

    last_name = forms.CharField(label='Фамилия', validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                                            message='Разрешены только кириллические '
                                                                                    'буквы, дефис и пробелы')],
                                error_messages={'required': 'Обязательное поле'})

    patronymic = forms.CharField(label='Отчество', required=False, validators=[RegexValidator('^[а-яА-Я- ]+$',
                                                                            message='Разрешены только кириллические '
                                                                                     'буквы, дефис и пробелы')])

    username = forms.CharField(label='Логин', validators=[RegexValidator('^[a-zA-Z-]+$',
                                                                         message='Разрешены только латиница и дефис')],
                               error_messages={
                                   'required': 'Обязательное поле',
                                   'unique': 'Данный логин уже занят'
                               })

    email = forms.EmailField(label='Электронная почта',
                             error_messages={
                                 'invalid': 'Не правильный формат',
                                 'unique': 'Данный почтовый адресс уже занят'
                             })

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                               error_messages={'required': 'Обязательное поле'})

    password2 = forms.CharField(label='Пароль (повтор)', widget=forms.PasswordInput,
                                error_messages={'required': 'Обязательное поле'})

    personal = forms.BooleanField(label='Согласие на обработку персональных данных', required=True,
                                  error_messages={'required': 'Обязательное поле'})

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Пароли не совпадают', code='password_nisnatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic',
                  'username', 'email', 'password', 'password2', 'personal')


class CreateApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class AddDesignApplications(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['design']


class AddCommentApplications(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['comment']
