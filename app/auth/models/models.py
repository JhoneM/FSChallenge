from ...conf.db import get_db, close_db
from flask import session

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)


class User:
    def __init__(
        self,
        user,
        password,
        re_password=False,
        name=False,
        last_name=False,
        level_id=False,
    ):
        self.user = user
        self.password = password
        self.re_password = re_password
        self.name = name
        self.last_name = last_name
        self.level_id = (
            self.get_level_admin() if not level_id else level_id
        )

    def register_new_user(self):
        db, c = get_db()
        msg = None
        new_user = False
        if self.user and self.password and self.name and self.last_name:
            c.execute(
                "SELECT id from user where username = %s", (self.user,)
            )
            if c.fetchone() is not None:
                msg = "Usuario {} se encuentra registrado.".format(
                    self.user
                )
            elif self.password != self.re_password:
                msg = "Las contraseñas no coinciden."
            else:
                if self.level_id:
                    c.execute(
                        """INSERT INTO user
                        (username,password,name,last_name,level_id)
                        values (%s, %s, %s, %s, %s)""",
                        (
                            self.user,
                            generate_password_hash(self.password),
                            self.name,
                            self.last_name,
                            self.level_id,
                        ),
                    )
                    db.commit()
                    msg = "Usuario Creado"
                    new_user = True
                else:
                    msg = "Error de sistema. Por favor verique \
                        que exista un nivel llamado 'usuario'."
        else:
            msg = "Error de sistema. Por favor verifique los datos."
        close_db()
        if msg:
            return msg, new_user

    def get_user(self, web=False):
        db, c = get_db()
        msg = None

        if self.user and self.password:
            c.execute(
                "SELECT * FROM user where username = %s", (self.user,)
            )
            user = c.fetchone()

            if user is None:
                msg = "Usuario y/o contraseña incorrecta"
            elif not check_password_hash(
                user["password"], self.password
            ):
                msg = "Usuario y/o contraseña invalida"
            elif user["active"] != 1:
                msg = "Usuario desactivado. Contacte al administrador."
            else:
                session.clear()
                session["user_id"] = user["id"]

            if web:
                if msg is None:
                    result = {
                        "status": "ok",
                        "id": user["id"],
                        "name_us": str(user["name"])
                        + " "
                        + str(user["last_name"]),
                    }
                else:
                    result = {"status": "error", "error_msg": msg}

                return result
            else:
                return msg

            close_db()

    def get_level_admin(self):
        db, c = get_db()
        query = "SELECT id FROM level_user where name='admin'"
        c.execute(query)
        value = c.fetchone()
        id = value["id"] or False
        close_db()
        return id
