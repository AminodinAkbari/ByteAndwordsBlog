from django import forms
from Comment.models import CommentModel
from captcha.fields import CaptchaField

class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = CommentModel
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }),
        }