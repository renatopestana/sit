from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ...extensions import db
from ...models import Project
from ...forms.projects import ProjectForm

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/", methods=["GET"])
@login_required
def list_():
    projects = Project.query.order_by(Project.name.asc()).all()
    return render_template("projects/list.html", projects=projects)

@projects_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        p = Project(name=form.name.data.strip(), description=form.description.data)
        db.session.add(p)
        db.session.commit()
        flash("Projeto salvo.", "success")
        return redirect(url_for("projects.list_"))
    return render_template("projects/form.html", form=form, mode="create")

@projects_bp.route("/<int:project_id>/editar", methods=["GET", "POST"])
@login_required
def edit(project_id):
    p = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash("Projeto atualizado.", "success")
        return redirect(url_for("projects.list_"))
    return render_template("projects/form.html", form=form, mode="edit", project=p)
