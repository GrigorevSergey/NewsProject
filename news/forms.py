from django.forms import ModelForm, BooleanField
from .models import Post


class PostForm(ModelForm):
    check = BooleanField(label='!!!!')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['title', 'text', 'Author', 'categoryContent', 'check']




