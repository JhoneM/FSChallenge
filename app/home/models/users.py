from ...conf.db import get_db, close_db
from ...auth.models.models import User as UserR
import logging

logging.basicConfig(level=logging.INFO)


class Users:
    def __init__(
        self, id=False, name=False, last_name=False, username=False
    ):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.username = username

    def get_all(self):
        db, c = get_db()

        query = """
        SELECT u.id,
        u.active as status,
        u.username,
        CONCAT(u.name, ' ', u.last_name) as complete_name,
        l.name as lvl_name,
        (SELECT IF(COUNT(id)>0, COUNT(id),"-")
            FROM account acc WHERE acc.user_id = u.id) as nro_acc
        FROM user AS u
        JOIN level_user AS l ON l.id = u.level_id
        """

        c.execute(query)
        values = c.fetchall()
        close_db()
        return values

    def get_all_levels(self):
        db, c = get_db()
        query = """
        SELECT * FROM level_user
        """
        c.execute(query)
        values = c.fetchall()
        close_db()
        return values

    def update_user(self):

        flag = False
        msg = _check_username_unique(self.username, self.id)
        if msg is not None:
            close_db()
            return msg, flag
        else:
            db, c = get_db()
            query = """
            UPDATE user SET username = %s, name = %s, last_name = %s
            WHERE id = %s
            """
            try:
                c.execute(
                    query,
                    (self.username, self.name, self.last_name, self.id),
                )

                db.commit()
                flag = True
                msg = (
                    "Usuario {} se ha actualizado exitosamente.".format(
                        self.username
                    )
                )

            except TypeError as e:
                flag = False
                msg = "Error al actualizar usuario -> %s" % e

            close_db()
            return msg, flag

    def deactivate_user(self, activate):
        db, c = get_db()
        status = "activado" if activate == 1 else "desactivado"
        flag = False

        query = """
        UPDATE user SET active = %s
        WHERE id = %s
        """
        try:
            c.execute(
                query,
                (activate, self.id),
            )

            db.commit()
            flag = True
            msg = "Usuario {} se ha {} exitosamente.".format(
                self.name, status
            )

        except TypeError as e:
            flag = False
            msg = "Error al actualizar usuario -> %s" % e

        close_db()
        return msg, flag

    def register_user(self, formData):
        user_register = UserR(
            formData["username"],
            formData["password"],
            formData["re_password"],
            formData["user_name"],
            formData["last_name"],
            formData["level"],
        )
        msg, new_user = user_register.register_new_user()
        return msg, new_user


def _check_username_unique(username, user_id):
    """
    Funcion para mostrar visualmente al usuario el error de username unico.
    Solo se ejecuta en el update ya que el registro tiene su validacion propia.
    """

    db, c = get_db()
    msg = None
    c.execute(
        "SELECT id from user where username = %s AND id != %s",
        (username, user_id),
    )

    if c.fetchone() is not None:
        msg = "El usuario {} se encuentra registrada.".format(username)

    close_db()
    return msg
