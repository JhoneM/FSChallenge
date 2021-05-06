from flask import render_template, jsonify, request
from datetime import datetime

from . import homes

from ..auth.conf.functions import login_required, check_level
from .models.users import Users
from .models.coins import Coins
from .models.transactions import Transactions
from .models.accounts import Account
from .models.operations import Operations

import logging

logging.basicConfig(level=logging.INFO)


@homes.route("/")
@login_required
def index():
    fecha = get_now_format_date()
    return render_template(
        "home/index.html", fecha=fecha, title="Inicio"
    )


# -------------------------
# ------- USERS -----------


@homes.route("/users")
@login_required
@check_level
def users():
    user = Users()
    users = user.get_all()
    levels = user.get_all_levels()
    return render_template(
        "home/users.html", values=users, levels=levels, title="Usuarios"
    )


@homes.route("/users/update", methods=["POST"])
@login_required
@check_level
def update_user():
    if request.method == "POST":
        user = False

        username = request.form["username"]
        user_id = request.form["user_id"]
        user_name = request.form["user_name"]
        user_lastname = request.form["last_name"]

        user_upd = Users(user_id, user_name, user_lastname, username)
        msg, user = user_upd.update_user()

        if user:
            return jsonify({"sucessul": msg})
        else:
            return jsonify({"error": msg})
    else:
        return jsonify({"error": "Error"})


@homes.route("/users/deactivate", methods=["POST"])
@login_required
@check_level
def deactivate_users():
    if request.method == "POST":
        user_id = request.form["user_id"]
        user_name = request.form["username"]
        activate = request.form["activate"]
        user_upd = Users(user_id, user_name)
        msg, user = user_upd.deactivate_user(activate)

        if user:
            return jsonify({"sucessul": msg})
        else:
            return jsonify({"error": msg})

    else:
        return jsonify({"error": "Error"})


@homes.route("/users/register", methods=["POST"])
@login_required
@check_level
def register_user():
    if request.method == "POST":
        formData = {
            "username": request.form["username"],
            "user_name": request.form["user_name"],
            "last_name": request.form["last_name"],
            "password": request.form["password"],
            "re_password": request.form["re_password"],
            "level": request.form["level"],
        }
        user_upd = Users()
        msg, user = user_upd.register_user(formData)
        if user:
            return jsonify({"sucessul": msg})
        else:
            return jsonify({"error": msg})
    else:
        return jsonify({"error": "Error"})


# -------------------------
# ------- COINS -----------


@homes.route("/coins")
@login_required
@check_level
def coins():
    coins = Coins().get_all()
    return render_template(
        "home/coins.html", values=coins, title="Monedas"
    )


@homes.route("/coins/update", methods=["POST"])
@login_required
@check_level
def update_coins():
    if request.method == "POST":
        coin = False

        coin_id = request.form["coinId"]
        coin_name = request.form["coinName"]
        coin_iso = request.form["coinIso"]

        coin_obj = Coins(coin_id, coin_name, coin_iso)
        msg, coin = coin_obj.update_coin()

        if coin:
            return jsonify({"sucessful": msg})
        else:
            return jsonify({"error": msg})
    else:
        return jsonify({"error": "Error"})


@homes.route("/coins/register", methods=["POST"])
@login_required
@check_level
def register_coins():
    if request.method == "POST":
        formData = {
            "coin_name": request.form["coinName"],
            "iso_code": request.form["isoCode"],
        }

        msg, coin = Coins().register_coin(formData)

        if coin:
            return jsonify({"sucessul": msg})
        else:
            return jsonify({"error": msg})
    else:
        return jsonify({"error": "Error"})


@homes.route("/coins/deactivate", methods=["POST"])
@login_required
@check_level
def deactivate_coins():
    if request.method == "POST":

        coin_id = request.form["coinId"]
        coin_name = request.form["coinName"]
        activate = request.form["activate"]

        msg, coin = Coins(coin_id, coin_name).deactivate_coin(activate)

        if coin:
            return jsonify({"sucessul": msg})
        else:
            return jsonify({"error": msg})

    else:
        return jsonify({"error": "Error"})


# -------------------------
# ------ ACCOUNTS ---------


@homes.route("/accounts")
@login_required
@check_level
def accounts():
    values = Account().get_all()
    return render_template(
        "home/accounts.html", values=values, title="Cuentas"
    )


# -------------------------
# ----- TRANSACTIONS ------


@homes.route("/transactions")
@login_required
@check_level
def transactions():
    values = Transactions().get_all()
    return render_template(
        "home/transactions.html", values=values, title="Transacciones"
    )


# -------------------------
# ----- OPERATIONS ------


@homes.route("/operations")
@login_required
@check_level
def operations():
    values = Operations().get_all()
    return render_template(
        "home/operations.html", values=values, title="Transacciones"
    )


# -------------------------
# ----- FUNCTIONS ---------


def get_now_format_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
