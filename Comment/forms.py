from django import forms
from Comment.models import CommentModel
from captcha.fields import CaptchaField

class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    content = forms.CharField(
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }
        )
    )
    class Meta:
        model = CommentModel
        fields = ['content']