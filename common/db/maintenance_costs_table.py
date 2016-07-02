# -*- coding: utf-8 -*-


class MaintenanceCostsTable:
    @classmethod
    def register(cls, cursor, bukken_id, management_costs, repair_costs):
        sql = 'select id from maintenance_cost where bukkenId = %s'
        cursor.execute(sql, (bukken_id))
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT prefecture SET managementConsts=%s, repairCosts=%s, bukkenId = %s'
        cursor.execute(sql, (management_costs, repair_costs, bukken_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from maintenance_cost'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select * from maintenance_cost where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row

    @classmethod
    def clearAll(cls, cursor):
        sql = 'delete from maintenance_cost'
        cursor.execute(sql)
