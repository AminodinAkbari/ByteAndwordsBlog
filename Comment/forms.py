from django import forms
from Comment.models import CommentModel

class CommentForm(forms.ModelForm):
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