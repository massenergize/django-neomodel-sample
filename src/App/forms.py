from django import forms

from App.models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('email', 'nickname', 'password', 'age_acknowledgment')
