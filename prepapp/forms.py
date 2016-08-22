from django import forms

from prepapp.models import Socio, Terreno, Tarifa, EscalonesEnergia, Items, Cesp


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
        fields = ['nroSocio', 'razonSocial', 'domicilio', 'localidad', 'telefono']

class TerrenosForm(MDLBaseModelForm):
    class Meta:
        model = Terreno
        fields = ['socio', 'nroTerreno', 'domicilio', 'condicionIva', 'nroMedidorEnergia', 'cargoConsumoAgua', 'tarifa']

class TarifasForm(MDLBaseModelForm):
    class Meta:
        model = Tarifa
        fields = ['nombre']

class EscalonesEnergiaForm(MDLBaseModelForm):
    class Meta:
        model = EscalonesEnergia
        fields = ['tarifa', 'desde', 'hasta', 'valor']

class ItemsForm(MDLBaseModelForm):
    class Meta:
        model = Items
        fields = ['nombre', 'tipo', 'aplicacion', 'valor']

class CespForm(MDLBaseModelForm):
    class Meta:
        model = Cesp
        fields = ['nroCesp', 'fecha']