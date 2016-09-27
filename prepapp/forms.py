# -*- coding: utf-8 -*-

from decimal import Decimal
from itertools import chain

from django import forms
from django.db import models
from django.forms import widgets, utils
from django.forms.fields import CharField
from django.forms.formsets import BaseFormSet
from django.utils import encoding, html, safestring

from prepapp import multiupload
from prepapp.models import Socio, Terreno, Tarifa, Escalones, Items, Cesp, AsociacionItemAgrupacion, AgrupacionDeItems


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
            return [getattr(obj, self.choices.queryset.model.fk_fields[0]), obj.pk]
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
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        if isinstance(self.field, BooleanFieldMDL):
            return ''
        elif isinstance(self.field, ChoiceFieldMDL):
            return super(BoundFieldMDL, self).label_tag(contents, attrs={'class': 'mdlext-selectfield__label'},
                                                        label_suffix=label_suffix)
        else:
            return super(BoundFieldMDL, self).label_tag(contents, attrs={'class': 'mdl-textfield__label'},
                                                        label_suffix=label_suffix)


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
    # def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text='',
    #              *args, **kwargs):
    #     if empty_label is not None:
    #         choices = tuple([(u'', empty_label)] + list(choices))
    #     else:
    #         choices = tuple([(u'', u'')] + list(choices))
    #     super(ChoiceFieldMDL, self).__init__(choices=choices, required=required, widget=widget, label=label,
    #                                          initial=initial, help_text=help_text, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(ChoiceFieldMDL, self).widget_attrs(widget)
        attrs.update({'style': 'width: 100%;'})
        return attrs


class AutoCompleteMDLFKField(forms.ModelChoiceField):
    widget = AutoCompleteFKMultiWidget


class BooleanFieldMDL(forms.BooleanField):
    class MDLSwitch(forms.CheckboxInput):
        def render(self, name, value, attrs=None):
            final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
            final_attrs['class'] = 'mdl-switch__input'
            if self.check_test(value):
                final_attrs['checked'] = 'checked'
            if not (value is True or value is False or value is None or value == ''):
                # Only add the 'value' attribute if a value is non-empty.
                final_attrs['value'] = encoding.force_text(value)
            wi = '<label class="mdl-switch mdl-js-switch" for="%s"><input {} ><span class="mdl-switch__label">%s</span></label>' % (
                'id_' + name, name)
            return html.format_html(wi, utils.flatatt(final_attrs))

    widget = MDLSwitch

    def widget_attrs(self, widget):
        attrs = super(BooleanFieldMDL, self).widget_attrs(widget)
        attrs.update({'class': 'mdl-switch__input'})
        return attrs
        return super(BooleanFieldMDL, self).widget_attrs(widget)


def customize_field(field):
    print field
    if field.choices:
        return ChoiceFieldMDL(choices=field.choices, label='', help_text=field.help_text)
    elif isinstance(field, models.CharField):
        return CharFieldMDL(max_length=field.max_length, help_text=field.help_text, required=not field.blank)
    elif isinstance(field, models.PositiveIntegerField) or isinstance(field, models.IntegerField):
        return IntegerFieldMDL(localize=False, help_text=field.help_text)
    elif isinstance(field, models.ForeignKey):
        return AutoCompleteMDLFKField(queryset=field.rel.to.objects.all())
    elif isinstance(field, models.BooleanField):
        return BooleanFieldMDL(help_text=field.help_text, required=not field.blank)
    else:
        return field.formfield()


class MDLBaseForm(forms.Form):
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
                        <div class ="mdl-textfield mdl-js-textfield mdlext-selectfield mdlext-js-selectfield" >
                            %(field)s
                            %(label)s
                        </div>
                        </div>
                        <span class="individual_errors">%(errors)s</span>
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
                        <div class ="mdl-textfield mdl-js-textfield mdlext-selectfield mdlext-js-selectfield" >
                            %(field)s
                            %(label)s
                        </div>
                        </div>
                        <span class="individual_errors">%(errors)s</span>
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
        fields = '__all__'
        exclude = ['activo']


class TarifaForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Tarifa
        fields = ['nombre']


class EscalasForm(forms.Form):
    escala = forms.ModelChoiceField(queryset=AgrupacionDeItems.objects.all(), widget=forms.HiddenInput(),
                                    required=False)
    desde = forms.IntegerField(required=True)
    hasta = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super(EscalasForm, self).clean()
        has = cleaned_data['hasta']
        des = cleaned_data['desde']
        if has < des:
            raise forms.ValidationError("El valor del campo 'hasta' no puede ser inferior al valor del campo 'desde'.")
        elif has == des:
            raise forms.ValidationError("El valor del campo 'desde' y 'hasta' no pueden ser iguales.")
        return cleaned_data


class ItemsEnergiaForm(forms.Form):
    asoc = forms.ModelChoiceField(queryset=AsociacionItemAgrupacion.objects.filter(item__aplicacion='EN'),
                                  widget=forms.HiddenInput(), required=False)
    item = forms.ModelChoiceField(queryset=Items.objects.filter(aplicacion='EN'),
                                  widget=AutoCompleteFKMultiWidget(attrs={'class': 'energia-item'}))
    # iva = forms.ChoiceField(choices=AsociacionItemAgrupacion.IVA_CHOICES,
    #                         widget=forms.Select(attrs={'class': 'energia-iva'}))
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'energia-valor'}))
    # escala = forms.IntegerField(widget=forms.HiddenInput())


class ItemsFijoForm(forms.Form):
    asoc = forms.ModelChoiceField(queryset=AsociacionItemAgrupacion.objects.filter(item__aplicacion='CF'),
                                  widget=forms.HiddenInput(), required=False)
    item = forms.ModelChoiceField(queryset=Items.objects.filter(aplicacion='CF'),
                                  widget=AutoCompleteFKMultiWidget(attrs={'class': 'fijos-item'}))
    # iva = forms.ChoiceField(choices=AsociacionItemAgrupacion.IVA_CHOICES,
    #                         widget=forms.Select(attrs={'class': 'fijos-iva'}))
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'fijos-valor'}))
    # escala = forms.IntegerField(widget=forms.HiddenInput())


class EscalonesForm(forms.Form):
    item = forms.IntegerField(widget=forms.HiddenInput())
    desde = forms.IntegerField()
    hasta = forms.IntegerField()
    valor = forms.DecimalField(decimal_places=5)


class ItemsForm(MDLBaseModelForm):
    formfield_callback = customize_field

    # activo = BooleanFieldMDL(required=False)
    # requerido = BooleanFieldMDL(required=False)

    class Meta:
        model = Items
        fields = '__all__'
        exclude = ['tarifa']


class CespForm(MDLBaseModelForm):
    formfield_callback = customize_field

    class Meta:
        model = Cesp
        fields = ['nroCesp', 'fecha']


class ImportacionAguaForm(MDLBaseForm):
    agua = multiupload.MultiFileField(required=True, label='')
    mes = ChoiceFieldMDL(choices=tuple([(item, item) for item in range(1, 13)]), required=True, label='')
    ano = CharFieldMDL(max_length=4, required=True, label='Año')

class escala_formset(BaseFormSet):
    def clean(self):
        i = 0
        hasta = 0
        for form in self.forms:
            if not form.cleaned_data:
                raise forms.ValidationError("Las escalas no pueden tener campos vacios.")
            # elif not form.cleaned_data['hasta']:
            #     raise forms.ValidationError("Campo 'hasta' vacio.")
            # elif not form.cleaned_data['desde']:
            #     raise forms.ValidationError("Campo 'desde' vacio.")

            if i > 0:
                desde = form.cleaned_data['desde']
                if desde == hasta+1:
                    hasta = form.cleaned_data['hasta']
                else:
                    raise forms.ValidationError("Las escalas no son correlativas entre si.")
                    hasta = form.cleaned_data['hasta']
            else:
                hasta = form.cleaned_data['hasta']
            i += 1
        return hasta
