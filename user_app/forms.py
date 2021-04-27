from django import forms

class ProcessingRequestForm(forms.Form):
    source_file_name = forms.CharField(label='Source filename', max_length=100)
    dest_file_name = forms.CharField(label='Destination filename', max_length=100)
    source_file_name = forms.CharField(label='Source filename', max_length=100)
