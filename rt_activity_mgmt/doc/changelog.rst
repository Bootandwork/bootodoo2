16.0.1 (5 Feb 2023)
-------

- Init version

16.0.2 (2 June 2023)
-------
- [bug] small bug fixed.

put hierarchize="0" select="one" in user_id filter of searchpanel

<field name="user_id"
hierarchize="0" select="one"
icon="fa-users" enable_counters="1" />

    
  File "C:\Program Files\Odoo 16.0\server\odoo\osv\expression.py", line 594, in parent_of_domain
    records = records[parent_name] - records.browse(parent_ids)
  File "C:\Program Files\Odoo 16.0\server\odoo\models.py", line 5759, in __sub__
    raise TypeError(f"inconsistent models in: {self} - {other}")
TypeError: inconsistent models in: res.partner() - res.users(2, 6)


16.0.3 (5 June 2023)
-------
- [add] Done Activity Logs

16.0.4 (21 Dec 2023)
-------
- [add] kanban, calendar, pivot, graph views for done activity logs
