from django import forms
from .models import Book, Author
from django.forms import ValidationError


class BookForm(forms.ModelForm):
    author = forms.CharField()
    published_date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'placeholder': '24.03.2025',
                'x-mask': '99.99.9999',
            }
        )
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_author(self):
        name = self.cleaned_data.get('author').strip()
        author, created = Author.objects.get_or_create(
            name__iexact=name, defaults={'name': name})
        return author
