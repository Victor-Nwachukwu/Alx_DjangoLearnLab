from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from .models import Tag
from taggit.forms import TagWidget 


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Separate tags with commas")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include 'tags' field
        widgets = {
            'tags': TagWidget(),  # use TagWidget for the tags field
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # only the text field should be edited
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content.strip()) < 2:
            raise forms.ValidationError("Comment must be at least 2 characters long.")
        return content