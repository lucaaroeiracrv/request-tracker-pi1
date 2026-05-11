import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from database import Database

load_dotenv()

app = Flask(__name__)


def get_env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente {key} não definida.")
    return value


def create_database() -> Database:
    return Database(
        host=get_env_or_raise("DB_HOST"),
        user=get_env_or_raise("DB_USER"),
        password=get_env_or_raise("DB_PASSWORD"),
        database=get_env_or_raise("DB_NAME"),
    )


def calculate_priority(urgency: int, impact: int) -> str:
    total = urgency + impact
    if total >= 5:
        return "Alta"
    if total >= 3:
        return "Média"
    return "Baixa"


def get_default_user_id(db: Database) -> int:
    result = db.execute_query("SELECT id FROM users ORDER BY id LIMIT 1")
    if not result:
        raise ValueError("Nenhum usuário cadastrado para associar a solicitação.")
    row = result[0]
    if isinstance(row, dict):
        return row.get("id")
    return row[0]


@app.route("/abrir")
def abrir():
    return render_template("abrir_solicitacao.html")


@app.route("/salvar", methods=["POST"])
def salvar():
    categoria = request.form.get("categoria", "").strip()
    descricao = request.form.get("descricao", "").strip()
    urgencia = request.form.get("urgencia", "").strip()
    impacto = request.form.get("impacto", "").strip()

    errors = []
    if not categoria:
        errors.append("Categoria é obrigatória.")
    if not descricao:
        errors.append("Descrição é obrigatória.")

    try:
        urgencia_value = int(urgencia)
        if urgencia_value not in (1, 2, 3):
            raise ValueError
    except ValueError:
        errors.append("Urgência deve ser um número entre 1 e 3.")

    try:
        impacto_value = int(impacto)
        if impacto_value not in (1, 2, 3):
            raise ValueError
    except ValueError:
        errors.append("Impacto deve ser um número entre 1 e 3.")

    if errors:
        return render_template(
            "abrir_solicitacao.html",
            errors=errors,
            categoria=categoria,
            descricao=descricao,
            urgencia=urgencia,
            impacto=impacto,
        )

    prioridade = calculate_priority(urgencia_value, impacto_value)

    try:
        db = create_database()
        with db:
            user_id = get_default_user_id(db)
            insert_query = """
                INSERT INTO requests
                    (user_id, category, description, urgency, impact, priority, status)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(
                insert_query,
                (
                    user_id,
                    categoria,
                    descricao,
                    urgencia_value,
                    impacto_value,
                    prioridade,
                    "Pendente",
                ),
            )
    except Exception as error:
        return render_template(
            "abrir_solicitacao.html",
            errors=[f"Não foi possível salvar a solicitação: {error}"],
            categoria=categoria,
            descricao=descricao,
            urgencia=urgencia,
            impacto=impacto,
        )

    return render_template(
        "abrir_solicitacao.html",
        success="Solicitação salva com sucesso!",
    )


@app.route("/style.css")
def serve_style():
    return send_from_directory(os.path.dirname(__file__), "style.css")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
