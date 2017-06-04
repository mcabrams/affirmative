from django import forms

from confirm.models import Confirmation

ConfirmFormset = forms.modelformset_factory(
    Confirmation,
    fields=('confirmed', 'src_path', 'dst_path',),
    widgets={'src_path': forms.TextInput(),
             'dst_path': forms.TextInput()},
    extra=0
)
