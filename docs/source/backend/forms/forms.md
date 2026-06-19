# Forms
Backend half of forms (there is also *[frontend part](../frontend/forms.md)*)

## Definition: Django Form:
A Python class that defines field behavior and validation rules for user inputs.

## Properties: Forms backend pieces
- `forms.py`: The standard location for form classes within a Django app.
- `forms.ModelForm`: Specialized form that maps directly to a Django Model.
- `forms.Form`: Standard form for inputs not tied to a database table.

## Workflow: Adding a `forms.ModelForm`
1. Identify the Model requiring user input.
2. Open `forms.py` and import dependencies:
    ```python
    from django import forms
    from .models import Book
    ```
3. Create the class with a `Meta` inner class:
    ```python
    class BookForm(forms.ModelForm):
        class Meta:
            model = Book
            fields = ['title', 'author']
    ```
4. Define `widgets` for field-specific attributes (placeholders, rows, or AlpineJS attrs):
    ```python
    widgets = {
        'text': forms.Textarea(attrs={
            'rows': 4, 
            'placeholder': 'Enter book description...'
        }),
        'published_date': forms.TextInput(attrs={
            'x-mask': '99/99/9999',
            'placeholder': 'MM/DD/YYYY'
        }),
    }
    ```
5. Use the form in `views.py`:
    ```python
    @require_POST
    def update_book(request, pk):
        book = Book.objects.get(pk=pk)
        form = BookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.save()
    ```


## Properties: Fields
- forms.CharField - A field for string input:
    ```python
    title = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label="Book Title"
    )
    ```
- forms.DateTimeField - A field for date and time input:
    ```python
    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now,
        label="Publication Date"
    )
    ```
- forms.ModelChoiceField - A ChoiceField whose choices are a model QuerySet:
    ```python
    author = forms.ModelChoiceField(
        queryset=Author.objects.all().order_by('name'),
        empty_label="Select an Author...",
        label="Author"
    )
    ```
- forms.ModelMultipleChoiceField - Allows selecting multiple instances:
    ```python
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Genres"
    )
    ```

## Workflow: Cleaning the data
1. Add method for field you want to clean
    ```python
    def clean_field_name(self):
        self.field_name = self.field_name.upper()
    ```
2. Call `full_clean()` before saving the model
    ```python
    
    ```