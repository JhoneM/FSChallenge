from flask import request, jsonify, session
from flask_cors import cross_origin
from werkzeug.exceptions import Forbidden
from ..auth.models.models import User
from ..home.models.transactions import Transactions
from ..home.models.accounts import Account
from . import web_client
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from .models.models import AccountUser, OperationsUser


@web_client.route("/login", methods=["POST"])
@cross_origin()
def login():
    username = request.json["username"] or False
    password = request.json["password"] or False
    web = True
    if username and password:
        user_login = User(username, password)
        result = user_login.get_user(web)
        if result["status"] == "ok":
            access_token = create_access_token(
                identity={
                    "id": result["id"],
                    "name_us": result["name_us"],
                }
            )
            result["access_token"] = access_token
    else:
        result = {
            "status": "error",
            "error_msg": "Hubo un error, por favor intente de nuevo.",
        }

    return jsonify(result)


@web_client.route("/register", methods=["POST"])
@cross_origin()
def register():
    username = request.json["username"] or False
    password = request.json["password"] or False
    re_password = request.json["re_password"] or False
    name = request.json["name"] or False
    last_name = request.json["last_name"] or False
    level_id = request.json["lvl_user"] or False

    new_user = False

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
            username, password, re_password, name, last_name, level_id
        )
        msg, new_user = user_register.register_new_user()

    result = {
        "status": "ok" if new_user else "error",
        "msg": msg,
    }

    return jsonify(result)


@web_client.route("/logout")
@cross_origin()
def logout():
    session.clear()
    return jsonify({"status": "ok"})


@web_client.route("/transactions", methods=["GET"])
@cross_origin()
@jwt_required()
def transactions():
    user = get_jwt_identity()
    if user:
        values = Transactions().get_all(user["id"])
        return jsonify(
            result={
                "transactions": values,
                "username": user["name_us"],
            }
        )
    else:
        raise Forbidden()


@web_client.route("/accounts", methods=["GET"])
@cross_origin()
@jwt_required()
def accounts():
    user = get_jwt_identity()
    if user:
        values = Account().get_all(user["id"])
        return jsonify(
            result={"accounts": values, "username": user["name_us"]}
        )
    else:
        raise Forbidden()


@web_client.route("/accounts_dis", methods=["GET"])
@cross_origin()
@jwt_required()
def accounts_dis():
    user = get_jwt_identity()
    if user:
        values = AccountUser().get_all(user["id"])
        return jsonify(result={"values": values})
    else:
        raise Forbidden()


@web_client.route("/accounts_dest", methods=["GET"])
@cross_origin()
@jwt_required()
def accounts_dest():
    user = get_jwt_identity()
    iso = request.args.get("iso") or False
    if user and iso:
        values = AccountUser().get_acc_dest(user["id"], iso)
        return jsonify(result={"accounts": values})
    else:
        raise Forbidden()


@web_client.route("/account_new_us", methods=["POST"])
@cross_origin()
@jwt_required()
def account_new_us():
    user = get_jwt_identity()
    coin_id = request.json["coin_id"] or False
    if user and coin_id:
        result = AccountUser().new_account(user["id"], coin_id)
        return jsonify(result)
    else:
        raise Forbidden()


@web_client.route("/operations_us", methods=["GET"])
@cross_origin()
@jwt_required()
def operations_us():
    user = get_jwt_identity()
    if user:
        values = OperationsUser().get_all()
        return jsonify(result={"operations": values})
    else:
        raise Forbidden()


@web_client.route("/acc_amount_max", methods=["GET"])
@cross_origin()
@jwt_required()
def acc_amount_max():
    user = get_jwt_identity()
    iso = request.args.get("iso") or False
    if user and iso:
        values = AccountUser().account_info(iso, user["id"])
        return jsonify(result={"account": values})
    else:
        raise Forbidden()


@web_client.route("/make_operation", methods=["POST"])
@cross_origin()
@jwt_required()
def make_operation():
    user = get_jwt_identity()

    iso_cta_org = request.json["cta_org"]
    cta_des = request.json["cta_dts"]
    operation = request.json["operation"]
    amount = request.json["amount"]
    if user:
        values = OperationsUser().make_operations(
            iso_cta_org, cta_des, operation, amount, user["id"]
        )
        return jsonify(result=values)
    else:
        result = {"status": "error", "msg": "Error en los datos"}
    return result
