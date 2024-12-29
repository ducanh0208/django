from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import Comment


def validate_file_type(value):
    """Custom validator for the file type."""
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'mp3', 'wav', 'xlsx', 'xls']
    ext = value.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'File type {ext} is not allowed. Allowed types are: {", ".join(valid_extensions)}.')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'file']
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write a comment...',
            'rows': 3,
        }),
        required=False
    )
    
    file = forms.FileField(
        required=False,
        validators=[validate_file_type],
        widget=forms.ClearableFileInput()
    )
