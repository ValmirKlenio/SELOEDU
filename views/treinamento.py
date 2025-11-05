from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from models.treinamento import Treinamento
from extensions import db
from datetime import datetime

@login_required
def listar():
    treinamentos = Treinamento.query.all()
    return render_template("treinamento/listar.html", treinamentos=treinamentos)

@login_required
def novo():
    if current_user.role != 'coordenador':
        abort(403)  # Forbidden

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        data_inicio_str = request.form.get("data_inicio")
        data_fim_str = request.form.get("data_fim")

        if not nome or not data_inicio_str:
            flash("Nome e Data de Início são obrigatórios!", "danger")
            return render_template("treinamento/novo.html", form_data=request.form)

        try:
            data_inicio = datetime.fromisoformat(data_inicio_str)
            data_fim = datetime.fromisoformat(data_fim_str) if data_fim_str else None
        except ValueError:
            flash("Formato de data inválido. Use YYYY-MM-DDTHH:MM.", "danger")
            return render_template("treinamento/novo.html", form_data=request.form)

        treinamento = Treinamento(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            coordenador_id=current_user.id
        )
        db.session.add(treinamento)
        db.session.commit()

        flash("Treinamento criado com sucesso!", "success")
        return redirect(url_for("treinamento.listar"))

    return render_template("treinamento/novo.html")
