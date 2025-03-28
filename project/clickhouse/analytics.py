from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError


def insert_habitation_view(
    engine: Engine,
    user_id: int,
    habitation_id: int
) -> None:
    """
    Вставляет запись в таблицу habitation_views
    """
    query = text(f"""
        INSERT INTO habitation_views
        (user_id, viewed_habitation_id, created_at)
        VALUES ({user_id}, {habitation_id}, NOW())
    """)

    connection = engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(query)
        transaction.commit()

    except SQLAlchemyError as e:
        transaction.rollback()
        print(f"Error on insert data in habitation_views: {str(e)}")

    finally:
        connection.close()


def insert_user_view(
    engine: Engine,
    user_id: int,
    viewed_user_id: int
) -> None:
    """
    Вставляет запись в таблицу user_views
    """
    query = text(f"""
        INSERT INTO user_views
        (user_id, viewed_user_id, created_at)
        VALUES ({user_id}, {viewed_user_id}, NOW())
    """)

    connection = engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(query)
        transaction.commit()

    except SQLAlchemyError as e:
        transaction.rollback()
        print(f"Error on insert data in user_views: {str(e)}")

    finally:
        connection.close()


def insert_filter_ei(
    engine: Engine,
    user_id: int,
    ei_id: int
) -> None:
    """
    Вставляет запись в таблицу user_filter_ei
    """
    query = text(f"""
        INSERT INTO user_filter_ei
        (user_id, filtered_ei_id, created_at)
        VALUES ({user_id}, {ei_id}, NOW())
    """)

    connection = engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(query)
        transaction.commit()

    except SQLAlchemyError as e:
        transaction.rollback()
        print(f"Error on insert data in user_filter_ei: {str(e)}")

    finally:
        connection.close()


def insert_filter_locality(
    engine: Engine,
    user_id: int,
    locality_id: int
) -> None:
    """
    Вставляет запись в таблицу user_filter_locality
    """
    query = text(f"""
        INSERT INTO user_filter_locality
        (user_id, filtered_locality_id, created_at)
        VALUES ({user_id}, {locality_id}, NOW())
    """)

    connection = engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(query)
        transaction.commit()

    except SQLAlchemyError as e:
        transaction.rollback()
        print(f"Error on insert data in user_filter_locality: {str(e)}")

    finally:
        connection.close()
