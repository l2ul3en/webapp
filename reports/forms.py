from django import forms

class ReportForm(forms.Form):
    #start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hostgroup = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        hostgroups = kwargs.pop('hostgroups', [])
        super().__init__(*args, **kwargs)
        self.fields['hostgroup'].choices = hostgroups