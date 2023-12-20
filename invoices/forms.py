from django import forms

from classes import CustomBaseForm
from .models import Invoice


class InvoiceForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define choices for the invoice_theme field
        self.fields['payment_status'].widget.choices = [
            ('PENDING', 'NEW'),
            ('PARTIALLY PAID', 'PARTIALLY PAID'),
            ('PAID', 'FULLY PAID'),
        ]

    # # Add a custom class to the <p> tag
    # def as_custom_p(self):
    #     return self._html_output(
    #         normal_row=''
    #                    '<div %(html_class_attr)s>'
    #                    '%(label)s'
    #                    '<br/>'
    #                    '%(field)s%(help_text)s'
    #                    '</div>'
    #                    '',
    #         error_row='%s',
    #         row_ender='</p>',
    #         help_text_html=' <span class="helptext">%s</span>',
    #         errors_on_separate_row=True,
    #     )
