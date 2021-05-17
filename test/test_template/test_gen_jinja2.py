from jinja2 import (Environment, FileSystemLoader)


def test_jinja2_import_macro():
    env = Environment(
        loader=FileSystemLoader(['/home/kevin/Project/Memflask/anki_convertor/test/resource/test_apkg',
                                 '/home/kevin/Project/Memflask/anki_convertor/macros']))
    template = env.get_template('1469988999268.jinja2')
    ret = template.render(Unit="this is card name",
                          Audio="./audio.mp3",
                          Question="hello worlds", Choices=['a', 'b', 'c'])
    print(ret)
