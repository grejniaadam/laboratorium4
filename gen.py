import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATES = ROOT / 'templates'
OUT = ROOT / 'generated' / 'serializers.py'

def main():
    iface = json.load(open(ROOT / 'interface.json', 'r', encoding='utf-8'))
    types = iface.get('types', [])

    # collect primitive types
    primitive_types = ['int32', 'uint8', 'uint32', 'float64', 'string']

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    tmpl = env.get_template('python_struct.jinja2')

    rendered = tmpl.render(types=types, primitive_types=primitive_types)

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(rendered)

    print('Generated', OUT)

if __name__ == '__main__':
    main()
