from parser import utils


def test_singleton_instances_have_the_same_id():
    first = utils.Singleton()

    second = utils.Singleton()

    assert id(first) == id(second)
