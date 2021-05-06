from ...conf.db import get_db, close_db


class Transactions:
    def get_all(self, user_id=False):
        db, c = get_db()

        query = """
        SELECT
        CONCAT(us.name, ' ', us.last_name) as user_name,
        IF(t.acc_dest_id IS NULL, op.name, CONCAT(
            op.name,', ',CONCAT(
                us_dest.name, ' ', us_dest.last_name
                )
            )
        ) AS op_name,
        c.iso_code AS acc_coin,
        t.amount,
        t.id,
        t.acc_amount_initial,
        t.acc_amount_final,
        DATE_FORMAT(t.create_at, '%d/%m/%Y %H:%i') AS date
        FROM transactions AS t
        JOIN operations AS op ON t.operation_id = op.id
        JOIN account AS acc ON t.account_id = acc.id
        JOIN user AS us ON acc.user_id = us.id
        JOIN coin AS c ON acc.coin_id = c.id
        LEFT JOIN account as acc_dest ON t.acc_dest_id = acc_dest.id
        LEFT JOIN user as us_dest ON acc_dest.user_id = us_dest.id
        """
        if user_id:
            query += """WHERE acc.user_id = %s ORDER BY date DESC"""
            c.execute(
                query,
                (user_id,),
            )
        else:
            query += """ORDER BY date DESC"""
            c.execute(query)

        values = c.fetchall()
        close_db()
        return values
