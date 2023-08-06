from typing import Any, List, Tuple

from pypadb.connection_pool import cursor_type, connection
from pypadb.utils.conditions import Limit
from pypadb.utils.enums import QueryModeEnum


def query(sql: str, kwargs: dict, data_type: Any, mode: QueryModeEnum) -> Tuple[Any, int]:
    result_set, last_row_id = execute(sql, kwargs, cursor_type())
    if result_set is None or len(result_set) == 0:
        return None, 0

    if mode == QueryModeEnum.One:
        return data_type(**result_set[0]), last_row_id
    elif mode == QueryModeEnum.Many:
        return [data_type(**i) for i in result_set], last_row_id


def execute(sql: str, kwargs: dict = None, cursor_type=None) -> Tuple[List, int]:
    conn = connection()
    with conn:
        cur = conn.cursor(cursor_type) if cursor_type else conn.cursor()
        cur.execute(sql, kwargs)
        conn.commit()
        return cur.fetchall(), cur.lastrowid


def parse_sql_batch(columns: List, data_list: List) -> Tuple[str, dict]:
    query_dict: dict = {}
    query_sql: str = ''
    for i, v in enumerate(data_list):
        data_dict: dict = v.dict()
        query_dict = {**query_dict, **{f'{arg}{i}': data_dict.get(arg) for arg in columns}}
        query_sql += '('
        for item in columns:
            query_sql += f'%({item}{i})s,'
        query_sql = query_sql.rstrip(',') + '),'
    return query_sql.rstrip(','), query_dict


def parse_sql_where(sql: str, conditions: dict, limit: Limit = None) -> str:
    if conditions:
        sql += ' where'
        for key in conditions:
            sql += f' {key}=%({key})s and'
        sql = sql.rstrip(' and')
    return sql + str(limit) if limit else sql


def parse_sql_update(sql, entity) -> Tuple[str, dict]:
    data_dict = entity.dict()
    query_dict: dict = {}
    salt = '_a_salt_that_never_duplicate'
    sql += ' set'
    for key in data_dict:
        if data_dict[key] or data_dict[key] == 0:
            sql += f' {key}=%({key}{salt})s,'
            query_dict[f'{key}{salt}'] = data_dict[key]
    return sql.rstrip(','), query_dict
