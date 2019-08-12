from collections.abc import Mapping

def get(dotted_name: str, data: Mapping):
    pass
def get_safe(dotted_name: str, data: Mapping):
    pass


def test_it():
    app = {
        'a': {
            'b': {
                'c': 55
            }
        }
    }

    get(app, "a.b.c") == app['a']['b']['c']
    get(app, "a") == app['a']
    
    get_safe(app, "a.b.f") == app.get('a', {}).get('b', {}).get('f')
