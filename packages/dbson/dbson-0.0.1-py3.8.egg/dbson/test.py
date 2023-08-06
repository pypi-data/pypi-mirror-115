from dbson.serializer import *
from dbson.deserializer import *
from dbson.client import *
from dbson.commands import *


def main():
    # a = {"name": "vasya", "age": {"sex": 12}, "parents": ["irina", "petr", None]}
    # with open('out.dd', 'wb') as f:
    #    serialize(a, f)
    # with open('out.dd', 'rb') as f:
    #    print(deserialize(f))

    conn = connect('localhost', 18889)
    conn.set(collection_name='people', object_name='sasha', data={
        'name': 'alexey',
        'parents': ['egor', 'vasya']
    })

    conn.set(collection_name='people', object_name='egor', selector='parents',
             result_of=construct_get(collection_name='people',
                                     object_name='sasha', selector='parents'))

    conn.set(collection_name='people', object_name='egor', selector='brother',
             result_of=construct_get(collection_name='people',
                                     object_name='sasha', selector='name'))

    print(conn.get(collection_name='people', object_name='egor')['data'])
    # {'brother': 'alexey', 'parents': ['egor', 'vasya']}

    print(conn.ping())


if __name__ == '__main__':
    main()
