from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, validators
from wtforms.validators import DataRequired, Regexp
from wtforms.fields import EmailField
from flask_babel import lazy_gettext as _

partners_list = [
    "POLIÉSTETICA",
    "CLAUDIA VIEIRA",
    "ELIA CAMÕES",
]

procedure_list = [
    _("Microcirurgia cosmética Consulta"),
    _("Micro lifting de sobrancelha"),
    _("Micro blefaroplastia superior"),
    _("Micro blefaroplastia inferior"),
    _("Lifting do terço médio e inferior"),
    _("Micro cervicoplastia (papada e pescoço)"),
    _("Micro implante de sobrancelha"),
    _("Laser CO2")
]


class PartnerShipForm(FlaskForm):
    class Meta:
        novalidate = True

    nome = StringField(
        label=_(u'Nome'),
        validators=[
            InputRequired(message=_(u"Este campo é obrigatório.")),
            validators.Length(min=4, max=25),
            Regexp(r'^[A-Za-zÀ-ÿ\s]+$', message=_(u"O nome pode conter apenas letras e espaços."))
        ],
        render_kw={"class": "form-control", "placeholder": _(u"Introduza o seu Nome")}
    )

    apelido = StringField(
        label=_(u'Apelido'),
        validators=[
            DataRequired(message=_(u"Este campo é obrigatório.")),
            validators.Length(min=3, max=25),
            Regexp(r'^[A-Za-zÀ-ÿ\s]+$', message=_(u"O nome pode conter apenas letras e espaços."))
        ],
        render_kw={"class": "form-control", "placeholder": _(u"Introduza o seu Apelido")}
    )
    tel = StringField(
        label=_(u'Telefone'),
        validators=[
            DataRequired(message=_(u"Este campo é obrigatório.")),
            validators.Length(min=9, max=14),
            Regexp(r'^\d+$', message=_("Apenas números são permitidos."))
        ],
        render_kw={
            "class": "form-control",
            "placeholder": _("Introduza o seu contacto telefónico"),
            "inputmode": "tel",
            "pattern": "\\d*"
        }
    )
    email = EmailField(
        label=_(u'Email'),
        validators=[
            DataRequired(message=_(u"Este campo é obrigatório.")),
            validators.Email(),
            validators.Length(min=6, max=35)
        ],
        render_kw={"class": "form-control", "placeholder": _("Introduza o seu Email"), "type": "email"}
    )
    partner_ship_list = SelectField(
        label=_(u'Parceiro(a)'),
        choices=[("", _("Selecione um parceiro(a)"))] + [(partner, partner) for partner in partners_list],
        validators=[DataRequired(message=_("Por favor, selecione um parceiro(a)."))],
        render_kw={
            "class": "input_class_selection form-control",
            "placeholder": _("Selecione um parceiro(a)")
        }
    )
    procedure_list = SelectField(
        label=_(u'Procedimento'),
        choices=[("", _("Selecione uma procedimento"))] + [(procedure, procedure) for procedure in
                                                           procedure_list],
        validators=[DataRequired(message=_("Por favor, selecione um procedimento."))],
        render_kw={"class": "input_class_selection form-control"}
    )
    checkbox = BooleanField(
        label=_(
            u'Eu concordo em partilhar minhas informações de contato com o propósito de ser contactado pela Santiclinic'),
        default=False,
        validators=[DataRequired(message=_("Por favor, aceite os termos de responsabilidade."))],
        render_kw={"class": "custom_checkbox form-check-input"}
    )
    submit = SubmitField(
        label=_(u'Enviar'),
        render_kw={"class": "input_class_submit btn-success"}
    )