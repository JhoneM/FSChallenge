from ...conf.db import get_db, close_db
import mysql.connector


class AccountUser:
    def get_all(self, user_id):
        db, c = get_db()

        query = """
        SELECT c.id, CONCAT(c.name,', ',c.iso_code) AS value
        FROM coin c
        WHERE id NOT IN (
            SELECT coin_id FROM account WHERE user_id = %s  
        ) AND c.active = 1
        """

        c.execute(
            query,
            (user_id,),
        )
        values = c.fetchall()
        close_db()
        return values

    def new_account(self, user_id, coin_id):
        db, c = get_db()

        query = """
        INSERT INTO `account` (
            `id`, `user_id`, `coin_id`, `balance`
            )
        VALUES (
            NULL, %s, %s, '0.00'
            );
        """
        try:
            c.execute(
                query,
                (
                    user_id,
                    coin_id,
                ),
            )

            db.commit()
            acc = True
            msg = "Moneda creda exitosamente."
        except TypeError as e:
            acc = False
            msg = "Error al crear moneda -> %s" % e

        result = {"acc": acc, "msg": msg}

        close_db()
        return result

    def get_acc_dest(self, user_id, iso):
        db, c = get_db()

        query = """
        SELECT CONCAT(
            CONCAT(us.name, ' ', us.last_name),
            ', ', c.iso_code) AS acc_name,
        acc.id
        FROM account AS acc
        JOIN user AS us ON acc.user_id = us.id
        JOIN coin AS c On acc.coin_id = c.id
        WHERE c.iso_code = %s
        AND acc.user_id != %s
        ORDER BY acc.id ASC
        """
        c.execute(
            query,
            (
                iso,
                user_id,
            ),
        )
        values = c.fetchall()
        close_db()
        return values

    def account_info(self, iso, user_id):
        db, c = get_db()

        query = """
        SELECT acc.id, acc.balance, acc.user_id, acc.coin_id
        FROM account AS acc
        JOIN coin AS c ON acc.coin_id = c.id
        WHERE acc.user_id = %s
        AND c.iso_code = %s
        """

        c.execute(
            query,
            (
                user_id,
                iso,
            ),
        )
        values = c.fetchone()
        close_db()
        return values

    def get_acc_id(self, acc_id):
        db, c = get_db()

        query = """
        SELECT * FROM account
        WHERE id = %s
        """

        c.execute(
            query,
            (acc_id,),
        )
        values = c.fetchone()
        close_db()
        return values


class OperationsUser:
    def get_all(self):
        db, c = get_db()

        query = """
        SELECT * FROM operations
        WHERE active = 1
        ORDER BY id ASC
        """
        c.execute(query)
        values = c.fetchall()
        close_db()
        return values

    def get_op_id(self, op_id):
        db, c = get_db()

        query = """
        SELECT * FROM operations
        WHERE id = %s
        """

        c.execute(
            query,
            (op_id,),
        )
        values = c.fetchone()
        close_db()
        return values

    def make_operations(self, iso, cta_des, operation, amount, user_id):
        db, c = get_db()

        acc_us = AccountUser().account_info(iso, user_id)
        acc_dest = (
            False if not cta_des else AccountUser().get_acc_id(cta_des)
        )
        operation = self.get_op_id(operation)

        if operation:
            if operation["type"] == 1 or operation["type"] == 2:
                if acc_us:
                    amount_init = acc_us["balance"]

                    if operation["type"] == 1:
                        amount_final = acc_us["balance"] + amount
                    elif operation["type"] == 2:

                        amount_final = acc_us["balance"] - amount

                    msg_acc = self.acc_upd_balance(
                        acc_us["id"], amount_final
                    )
                    msg_op = self.execute_operation(
                        operation["id"],
                        acc_us["id"],
                        amount_init,
                        amount_final,
                        amount,
                    )
                    if msg_acc:
                        result = {
                            "status": "error",
                            "error_msg": msg_acc,
                        }
                        return result
                    if msg_op:
                        result = {
                            "status": "error",
                            "error_msg": msg_op,
                        }
                        return result
                else:
                    result = {
                        "status": "error",
                        "error_msg": "Error de cuentas.",
                    }
                    return result
            elif operation["type"] == 3:
                if acc_us and acc_dest:
                    amount_init_org = acc_us["balance"]
                    amount_final_org = acc_us["balance"] - amount
                    amount_init_dest = acc_dest["balance"]
                    amount_final_dest = acc_dest["balance"] + amount

                    msg_acc_org = self.acc_upd_balance(
                        acc_us["id"], amount_final_org
                    )

                    if msg_acc_org:
                        result = {
                            "status": "error",
                            "error_msg": msg_acc_org,
                        }
                        return result

                    msg_op_org = self.execute_operation(
                        operation["id"],
                        acc_us["id"],
                        amount_init_org,
                        amount_final_org,
                        amount,
                        acc_dest["id"],
                    )

                    if msg_op_org:
                        result = {
                            "status": "error",
                            "error_msg": msg_op_org,
                        }
                        return result

                    msg_acc_dest = self.acc_upd_balance(
                        acc_dest["id"], amount_final_dest
                    )

                    if msg_acc_dest:
                        result = {
                            "status": "error",
                            "error_msg": msg_acc_dest,
                        }
                        return result

                    msg_op_dest = self.execute_operation(
                        operation["id"],
                        acc_dest["id"],
                        amount_init_dest,
                        amount_final_dest,
                        amount,
                        acc_us["id"],
                    )

                    if msg_op_dest:
                        result = {
                            "status": "error",
                            "error_msg": msg_op_dest,
                        }
                        return result
                else:
                    result = {
                        "status": "error",
                        "error_msg": "Error de cuentas.",
                    }
                    return result
        else:
            result = {
                "status": "error",
                "error_msg": "Error en tipo de operacion.",
            }
            return result

        result = {"status": "ok", "msg": "Operacion realizada."}
        close_db()
        return result

    def acc_upd_balance(self, acc_id, balance):
        db, c = get_db()
        msg = None
        query = """
        UPDATE account set balance = %s
        WHERE id = %s
        """
        try:

            c.execute(
                query,
                (balance, acc_id),
            )
            db.commit()

        except mysql.connector.Error as err:
            msg = str(err.msg)

        close_db()
        return msg

    def execute_operation(
        self,
        ope_id,
        acc_id,
        amount_init,
        amount_final,
        amount,
        acc_dest=None,
    ):
        db, c = get_db()
        msg = None

        query = """
        INSERT INTO transactions (
            operation_id, account_id,
            acc_amount_initial, acc_amount_final, acc_dest_id,
            amount
            )
        VALUES (
            %s, %s, %s, %s, %s, %s
        )
        """
        try:
            c.execute(
                query,
                (
                    ope_id,
                    acc_id,
                    amount_init,
                    amount_final,
                    acc_dest,
                    amount,
                ),
            )
            db.commit()

        except mysql.connector.Error as err:
            msg = str(err.msg)

        close_db()
        return msg
