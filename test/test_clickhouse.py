from project.clickhouse.analytics import (insert_filter_ei,
                                          insert_filter_locality,
                                          insert_habitation_view,
                                          insert_user_view)
from project.clickhouse_database import get_olap

if __name__ == "__main__":
    engine = next(get_olap())

    insert_user_view(engine, 123, 321)
    print("insert_user_view")

    insert_habitation_view(engine, 321, 111)
    print("insert_habitation_view")

    insert_filter_ei(engine, 123, 212)
    print("insert_filter_ei")

    insert_filter_locality(engine, 111, 222)
    print("insert_filter_locality")
