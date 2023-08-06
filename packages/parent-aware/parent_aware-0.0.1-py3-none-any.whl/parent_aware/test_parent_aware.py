import dataclasses

from .parent_aware import parent_aware

def test_simple_parent():

    @parent_aware
    @dataclasses.dataclass
    class Child:
        num: int

    @parent_aware
    @dataclasses.dataclass
    class Parent:
        child: Child

    c = Child(2)
    p = Parent(child=c)

    assert c.parents == [p]


def test_simple_parent_other_name():

    @parent_aware(parents_name='the_parents')
    @dataclasses.dataclass
    class Child:
        num: int

    @parent_aware(parents_name='the_parents')
    @dataclasses.dataclass
    class Parent:
        child: Child

    c = Child(2)
    p = Parent(child=c)

    assert c.the_parents == [p]


def test_simple_parent_grand_child():
    @parent_aware
    @dataclasses.dataclass
    class GreatGrandChild:
        num: int

    @parent_aware
    @dataclasses.dataclass
    class GrandChild:
        great_grand_child: GreatGrandChild

    @parent_aware
    @dataclasses.dataclass
    class Child:
        grand_child: GrandChild

    @parent_aware
    @dataclasses.dataclass
    class Parent:
        child: Child

    gg = GreatGrandChild(3)
    g = GrandChild(gg)
    c = Child(g)
    p = Parent(child=c)

    assert gg.parents == [g, c, p]
    assert g.parents == [c, p]
    assert c.parents == [p]


def test_two_parents_one_child():
    @parent_aware
    @dataclasses.dataclass
    class Child:
        pass

    @parent_aware
    @dataclasses.dataclass
    class Parent:
        child: Child
        other: int

    c = Child()
    p1 = Parent(child=c, other=1)
    p2 = Parent(child=c, other=2)

    assert c.parents == [p1, p2]


def test_child_in_list():
    @parent_aware
    @dataclasses.dataclass
    class Child:
        num: int

    @parent_aware
    @dataclasses.dataclass
    class Parent:
        child: dataclasses.field(default_factory=list)

    c1 = Child(1)
    c2 = Child(2)

    p = Parent(child=[c1, c2])

    c1.parents == [p]
    c2.parents == [p]


def test_child_in_dict():
    @parent_aware
    @dataclasses.dataclass
    class Child:
        num: int

    @parent_aware
    @dataclasses.dataclass
    class Parent:
        child: dataclasses.field(default_factory=dict)

    c1 = Child(1)
    c2 = Child(2)

    p = Parent(child={
        'c1' : c1,
        'c2' : c2
    })

    c1.parents == [p]
    c2.parents == [p]