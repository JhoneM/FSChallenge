from flask import (
    flash,
    g,
    render_template,
    request,
    url_for,
    session,
    redirect,
)


from ..conf.db import get_db
from . import auths
from .models.models import User


@auths.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"] or False
        password = request.form["password"] or False
        re_password = request.form["re_password"] or False
        name = request.form["name"] or False
        last_name = request.form["last_name"] or False

        msg = None
        if (
            not username
            and not password
            and not re_password
            and not name
            and not last_name
        ):
            msg = "Hubo un error con los valores. Intente de nuevo."
        else:
            user_register = User(
                username, password, re_password, name, last_name
            )
            msg, new_user = user_register.register_new_user()

        if new_user:
            flash(msg)
            return redirect(url_for("auth.login"))

        flash(msg)
    # return render_template("auths/register.html", title="Registro")


@auths.route("/login", methods=["GET", "POST"])
def login():
    if not g.user:
        if request.method == "POST":
            username = request.form["username"] or False
            password = request.form["password"] or False

            if username and password:
                user_login = User(username, password)
                msg = user_login.get_user()
            else:
                msg = "Hubo un error, por favor intente de nuevo."

            if msg is None:
                return redirect(url_for("home.index"))
            flash(msg)
        return render_template("auths/login.html", title="Ingreso")
    else:
        return redirect(url_for("home.index"))


@auths.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auths.before_app_request
def load_logger_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute("SELECT * FROM user where id = %s", (user_id,))
        g.user = c.fetchone()
