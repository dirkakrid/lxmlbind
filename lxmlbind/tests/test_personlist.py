from copy import deepcopy
from nose.tools import assert_raises, eq_, ok_
from six import b

from lxmlbind.api import List, of, tag
from lxmlbind.tests.test_person import Person


@tag("person-list")
@of(Person)
class PersonList(List):
    """
    Example using typed list.
    """
    pass


def test_person_list():
    """
    Verify list operations.
    """
    person1 = Person()
    person1.first = "John"

    person2 = Person()
    person2.first = "Jane"

    # test append and __len__
    person_list = PersonList()
    eq_(len(person_list), 0)
    person_list.append(person1)
    eq_(len(person_list), 1)
    eq_(person1._parent, person_list)

    person_list.append(person2)
    eq_(len(person_list), 2)
    eq_(person2._parent, person_list)

    eq_(person_list.to_xml(),
        b("""<person-list><person type="object"><first>John</first></person><person type="object"><first>Jane</first></person></person-list>"""))  # noqa

    # test that append is preserving order
    person1_copy = deepcopy(person1)
    person2_copy = deepcopy(person2)
    person_list_reverse = PersonList()
    person_list_reverse.append(person2_copy)
    person_list_reverse.append(person1_copy)
    eq_(person_list[0], person_list_reverse[1])
    eq_(person_list[1], person_list_reverse[0])
    eq_(person_list_reverse.to_xml(),
        b"""<person-list><person type="object"><first>Jane</first></person><person type="object"><first>John</first></person></person-list>""")  # noqa

    # test that append is preserving order
    person1_copy = deepcopy(person1)
    person2_copy = deepcopy(person2)
    person_list_reverse = PersonList()
    person_list_reverse.append(person2_copy)
    person_list_reverse.append(person1_copy)
    eq_(person_list[0], person_list_reverse[1])
    eq_(person_list[1], person_list_reverse[0])
    eq_(person_list_reverse.to_xml(),
        b"""<person-list><person type="object"><first>Jane</first></person><person type="object"><first>John</first></person></person-list>""")  # noqa

    # test __getitem__
    eq_(person_list[0].first, "John")
    eq_(person_list[0]._parent, person_list)
    eq_(person_list[1].first, "Jane")
    eq_(person_list[0]._parent, person_list)

    # test __iter__
    eq_([person.first for person in person_list], ["John", "Jane"])
    ok_(all([person._parent == person_list for person in person_list]))

    # test __delitem__
    with assert_raises(IndexError):
        del person_list[2]
    del person_list[1]
    eq_(len(person_list), 1)
    eq_(person_list.to_xml(),
        b("""<person-list><person type="object"><first>John</first></person></person-list>"""))

    # test __setitem__
    person_list[0] = person2
    eq_(person_list.to_xml(),
        b("""<person-list><person type="object"><first>Jane</first></person></person-list>"""))
