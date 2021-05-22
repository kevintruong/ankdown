import os

from jinja2 import (Environment, FileSystemLoader)


def test_jinja2_import_macro():
    cur_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader([os.path.join(cur_dir, '../resource/test_apkg/'),
                                               os.path.join(cur_dir, '../../macros'),
                                               cur_dir
                                               ])
                      )
    template = env.get_template('1469988999268.jinja2')
    ret = template.render(Unit="this is card name",
                          Audio="./audio.mp3",
                          Question="hello worlds", Choices=['a', 'b', 'c'])
    print(ret)
