from django import forms

from prepapp.models import Socio


class MDLBaseModelForm(forms.ModelForm):
    class Meta:
        abstract = True

    def as_mdl(self):
        self.label_suffix = ''
        line = """<div class="row">
                    <div class="col s4">
                        <div class="input-field">
                            %(field)s
                            %(label)s
                            <span class="individual_errors">%(errors)s</span>
                        </div>
                    </div>
                    <div class="col s4">
                        %(help_text)s
                    </div>
                </div>"""
        return self._html_output(
            normal_row=line,
            error_row='<div class="form_errors">%s</div>',
            row_ender='</p>',
            help_text_html='<p class="help-text">%s</p>',
            errors_on_separate_row=False)

class SociosForm(MDLBaseModelForm):
    class Meta:
        model = Socio
        fields = ['nroSocio', 'razonSocial', 'domicilio', 'localidad']
