from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ...extensions import db
from ...models import Client
from ...forms.clients import ClientForm

clients_bp = Blueprint("clients", __name__)

@clients_bp.route("/", methods=["GET"])
@login_required
def list_():
    q = request.args.get("q", "").strip()
    query = Client.query
    if q:
        query = query.filter(Client.nome_razao.ilike(f"%{q}%"))
    clients = query.order_by(Client.created_at.desc()).all()
    return render_template("clients/list.html", clients=clients, q=q)

@clients_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    form = ClientForm()
    if form.validate_on_submit():
        c = Client(
            tipo=form.tipo.data,
            nome_razao=form.nome_razao.data.strip(),
            endereco=form.endereco.data.strip(),
            nacionalidade=form.nacionalidade.data,
            estado_civil=form.estado_civil.data,
            profissao=form.profissao.data,
            rg=form.rg.data,
            orgao_emissor_rg=form.orgao_emissor_rg.data,
            cpf=form.cpf.data,
            email=form.email.data,
            telefone=form.telefone.data,
            cnpj=form.cnpj.data,
            representante_nome=form.representante_nome.data,
            representante_email=form.representante_email.data,
            representante_telefone=form.representante_telefone.data,
            representante_funcao=form.representante_funcao.data,
        )
        db.session.add(c)
        db.session.commit()
        flash("Cliente salvo com sucesso.", "success")
        return redirect(url_for("clients.list_"))
    return render_template("clients/form.html", form=form, mode="create")

@clients_bp.route("/<int:client_id>/editar", methods=["GET", "POST"])
@login_required
def edit(client_id):
    c = Client.query.get_or_404(client_id)
    form = ClientForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.commit()
        flash("Cliente atualizado.", "success")
        return redirect(url_for("clients.list_"))
    return render_template("clients/form.html", form=form, mode="edit", client=c)
