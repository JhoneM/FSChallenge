from ...conf.db import get_db, close_db


class Account:
    def get_all(self, user_id=False):
        db, c = get_db()

        query = """
        SELECT
        CONCAT(us.name, ' ', us.last_name) as user_name,
        c.iso_code,
        acc.balance,
        acc.id AS acc_id,
        (SELECT CONCAT(op.name,' por ', t.amount, ' el ',
        DATE_FORMAT(t.create_at, '%d/%m/%Y %H:%i'))
        FROM transactions AS t
        JOIN operations AS op ON t.operation_id = op.id
        WHERE t.account_id = acc.id
        ORDER BY t.id DESC
        LIMIT 1 ) AS last_transaction
        FROM account AS acc
        JOIN user AS us ON acc.user_id = us.id
        JOIN coin AS c ON acc.coin_id = c.id
        """
        if user_id:
            query += """WHERE acc.user_id = %s ORDER BY acc_id ASC"""
            c.execute(
                query,
                (user_id,),
            )
        else:
            query += """ORDER BY acc_id ASC"""
            c.execute(query)

        values = c.fetchall()
        close_db()
        return values
