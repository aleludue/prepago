from django import forms
from django.db import models
from django.forms import widgets
from django.forms.fields import CharField

from prepapp.models import Socio, Terreno, Tarifa, Escalones, Items, Cesp, AsociacionItemAgrupacion


def charfield_handler(field):
    attrs = {}
    if field.max_length > 0:
        if field.min_length >= 0:
            attrs.update(
                {'data-validation': 'length', 'data-validation-length': '%s-%s' % (field.min_length, field.max_length)})
        else:
            attrs.update({'data-validation': 'length', 'data-validation-length': 'max%s' % field.max_length})
    elif field.required:
        attrs.update({'data-validation': 'required'})
    return attrs


#####   WIDGET's    #####

class AutoCompleteFKMultiWidget(widgets.MultiWidget):
    dict_pk_search = {}

    def __init__(self, attrs=None):
        _widgets = (
            widgets.TextInput(attrs={'class': 'mdl-textfield__input'}), widgets.HiddenInput())
        super(AutoCompleteFKMultiWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            obj = self.choices.queryset.model.objects.get(pk=value)
            return [getattr(obj, self.dict_pk_search[self.choices.queryset.model]), obj.pk]
        else:
            return [None, None]

    def value_from_datadict(self, data, files, name):
        values = super(AutoCompleteFKMultiWidget, self).value_from_datadict(data, files, name)
        try:
            return int(values[1])
        except ValueError:
            return None


#####   FIELD's     #####

class BoundFieldMDL(forms.forms.BoundField):
    def label_tag(self, contents=None, attrs={'class': 'mdl-textfield__label'}, label_suffix=None):
        return super(BoundFieldMDL, self).label_tag(contents, attrs, label_suffix)


class CharFieldMDL(forms.CharField):
    def widget_attrs(self, widget):
        attrs = super(CharFieldMDL, self).widget_attrs(widget)
        attrs.update({'class': 'mdl-textfield__input'})
        return attrs


class IntegerFieldMDL(forms.IntegerField):
    def widget_attrs(self, widget):
        attrs = super(IntegerFieldMDL, self).widget_attrs(widget)
        attrs.update({'class': 'mdl-textfield__input'})
        return attrs


class ChoiceFieldMDL(forms.ChoiceField):
    def widget_attrs(self, widget):
        attrs = super(ChoiceFieldMDL, self).widget_attrs(widget)
        attrs.update({'style': 'width: 100%;'})
        return attrs


class AutoCompleteMDLFKField(forms.ModelChoiceField):
    widget = AutoCompleteFKMultiWidget


def customize_field(field):
    if field.choices:
        return ChoiceFieldMDL(choices=field.choices, label='', help_text=field.help_text)
    elif isinstance(field, models.CharField):
        return CharFieldMDL(max_length=field.max_length, help_text=field.help_text)
    elif isinstance(field, models.PositiveIntegerField) or isinstance(field, models.IntegerField):
        return IntegerFieldMDL(localize=False, help_text=field.help_text)
    elif isinstance(field, models.ForeignKey):
        return AutoCompleteMDLFKField(queryset=field.rel.to.objects.all())
    else:
        return field.formfield()


class MDLBaseModelForm(forms.ModelForm):
    def __getitem__(self, name):
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(
                "Key %r not found in '%s'" % (name, self.__class__.__name__))
        if name not in self._bound_fields_cache:
            self._bound_fields_cache[name] = BoundFieldMDL(self, field, name)
        return self._bound_fields_cache[name]

    class Meta:
        abstract = True

    def as_mdl(self):
        self.label_suffix = ''
        line = """<div class="mdl-grid">
                    <div class="mdl-cell">
                        <div class="mdl-textfield mdl-js-textfield">
                            %(field)s
                            %(label)s
                            <span class="individual_errors">%(errors)s</span>
                        </div>
                    </div>
                    <div class="mdl-cell--8-col">
                        %(help_text)s
                    </div>
                </div>"""
        return self._html_output(
            normal_row=line,
            error_row='<div class="form_errors">%s</div>',
            row_ender='</p>',
            help_text_html='<p class="mdl-textfield mdl-js-textfield">%s</p>',
            errors_on_separate_row=False)


class SociosForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Socio
        fields = ['nroSocio', 'razonSocial', 'domicilio', 'localidad', 'telefono']


class TerrenosForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Terreno
        fields = ['socio', 'nroTerreno', 'domicilio', 'condicionIva', 'nroMedidorEnergia', 'cargoConsumoAgua']


class TarifaForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Tarifa
        fields = ['nombre']

class EscalasForm(forms.Form):
    desde = forms.IntegerField()
    hasta = forms.IntegerField()


class ItemsEnergiaForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Items.objects.filter(aplicacion='EN'), widget=AutoCompleteFKMultiWidget())
    iva = forms.ChoiceField(choices=AsociacionItemAgrupacion.IVA_CHOICES)
    valor = forms.DecimalField(max_digits=5)
    escala = forms.IntegerField(widget=forms.HiddenInput())


class ItemsFijoForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Items.objects.filter(aplicacion='CF'), widget=AutoCompleteFKMultiWidget())
    iva = forms.ChoiceField(choices=AsociacionItemAgrupacion.IVA_CHOICES)
    valor = forms.DecimalField(max_digits=5)
    escala = forms.IntegerField(widget=forms.HiddenInput())


class EscalonesForm(forms.Form):
    item = forms.IntegerField(widget=forms.HiddenInput())
    desde = forms.IntegerField()
    hasta = forms.IntegerField()
    valor = forms.DecimalField(decimal_places=5)


# class ItemsForm(MDLBaseModelForm):
#     class Meta:
#         model = Items
#         fields = ['nombre', 'tipo', 'aplicacion', 'valor']


class CespForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Cesp
        fields = ['nroCesp', 'fecha']
