from django import forms
from .models import User , Post
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

            






class LoginForm(AuthenticationForm):
        username = forms.CharField(max_length=250, required=True,
                                    widget=forms.TextInput,label='Phone or username ') 
        password = forms.CharField(required=True, max_length=250)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20,widget=forms.PasswordInput, label="رمز عبور")
    password2 = forms.CharField(max_length=20,widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ['username','last_name','first_name','phone']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("رمز عبور با تکرار آن مطابقت ندارد")
        # این قانونه جنگو هست که pass2 رو ret کنی
        return cd['password2']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره تلفن قبلا ثبت شده است")
        return phone




class UserEditFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','date_of_birth','photo','job','bio','phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("این شماره تلفن قبلا ثبت شده است")
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلا ثبت شده است")
        return username



class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    
    message = forms.CharField( widget=forms.Textarea, required=True )
    name = forms.CharField(max_length=250 ,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11 ,required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError("شماره تلفن عددی نیست!")
        if len(phone) != 11:
            raise forms.ValidationError("شماره تلفن باید 11 رقمی باشد!")
        return phone
    
    def clean_message(self):
        message = self.cleaned_data['message']
        # بررسی اینکه پیام خالی نباشد و حداقل ۱۰ کاراکتر داشته باشد
        if len(message.strip()) < 3:
            raise forms.ValidationError("پیام باید حداقل 3 کاراکتر داشته باشد!")
        return message

    def clean_name(self):
        name = self.cleaned_data['name']
        # بررسی اینکه نام خالی نباشد و حداقل ۳ کاراکتر داشته باشد
        if len(name.strip()) < 3:
            raise forms.ValidationError("نام باید حداقل ۳ کاراکتر داشته باشد!")
        return name
    



class CreatePostForm(forms.ModelForm):
    class Meta:
            model = Post
            fields = ['description', 'tags']
