from django import forms

class SignInForm(forms.Form):
    username = forms.CharField(
        label="Email / Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Email or Username",
            "class": "w-full px-4 py-3 border-2 text-black bg-[#7AABF5] rounded-2xl focus:outline-none focus:border-[#097AFA] placeholder-black"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password",
            "class": "w-full px-4 py-3 border-2 text-black bg-[#7AABF5] rounded-2xl focus:outline-none focus:border-[#097AFA] placeholder-black"
        })
    )
