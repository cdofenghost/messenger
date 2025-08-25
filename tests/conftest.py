from ..backend.database import get_engine, Base

def flush_database():
    Base.metadata.drop_all(bind=get_engine())
    Base.metadata.create_all(bind=get_engine())


funcs_of_interest = ["test_register", "test_register2"]

def pytest_runtest_teardown(item, nextitem):
    curr_name = item.function.__qualname__
    if curr_name in funcs_of_interest:
        if nextitem is not None:
            next_name = nextitem.function.__qualname__
        else:
            next_name = "random_name"
        if curr_name != next_name:
            flush_database()