from ...conf.db import get_db, close_db
import logging

logging.basicConfig(level=logging.INFO)


class Coins:
    def __init__(self, id=False, name=False, iso_code=False):
        self.id = id
        self.name = name
        self.iso_code = iso_code

    def get_all(self):
        db, c = get_db()
        query = """
        SELECT * FROM coin
        """
        c.execute(query)
        values = c.fetchall()
        close_db()
        return values

    def update_coin(self):

        coin = False

        msg = _check_iso_unique(self.iso_code, self.name, self.id)
        if msg is not None:
            close_db()
            return msg, coin

        else:
            db, c = get_db()
            query = """
            UPDATE coin SET name = %s, iso_code = %s
            WHERE id = %s
            """
            try:
                c.execute(
                    query,
                    (self.name, self.iso_code.upper(), self.id),
                )

                db.commit()
                coin = True
                msg = "La moneda {} se ha actualizado exitosamente.".format(
                    self.name
                )

            except TypeError as e:
                coin = False
                msg = "Error al actualizar moneda -> %s" % e

            close_db()
            return msg, coin

    def register_coin(self, formData):
        coin = False
        msg = _check_iso_unique(formData["iso_code"])
        if msg is not None:

            close_db()
            return msg, coin

        else:
            db, c = get_db()
            query = (
                """INSERT INTO coin (name, iso_code) VALUES (%s,%s)"""
            )
            try:
                c.execute(
                    query,
                    (
                        formData["coin_name"],
                        formData["iso_code"].upper(),
                    ),
                )

                db.commit()
                coin = True
                msg = "Moneda creda exitosamente."
            except TypeError as e:
                coin = False
                msg = "Error al cread moneda -> %s" % e

            close_db()
            return msg, coin

    def deactivate_coin(self, activate):
        db, c = get_db()
        status = "activado" if activate == "1" else "desactivado"

        coin = False

        query = """
        UPDATE coin SET active = %s
        WHERE id = %s
        """
        try:
            c.execute(
                query,
                (activate, self.id),
            )

            db.commit()
            coin = True
            msg = "La moneda {} se ha {} exitosamente.".format(
                self.name, status
            )

        except TypeError as e:
            coin = False
            msg = "Error al actualizar usuario -> %s" % e

        close_db()
        return msg, coin


def _check_iso_unique(iso_code, coin_id=False):
    """
    Funcion para mostrar visualmente al usuario el error de iso_code unico.
    Si existe coin_id es una actualizacion, de lo contrario
    es un nuevo registro.
    """

    db, c = get_db()
    msg = None
    if not coin_id:
        c.execute(
            "SELECT id from coin where iso_code = %s",
            (iso_code,),
        )
    else:
        c.execute(
            "SELECT id from coin where iso_code = %s AND id != %s",
            (iso_code, coin_id),
        )

    if c.fetchone() is not None:
        msg = "La moneda {} se encuentra registrado.".format(iso_code)
    close_db()
    return msg
