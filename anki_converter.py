import os

from anki2 import Apkg
import click


@click.group()
def command():
    pass


@click.command()
@click.argument("apkg_file", default=None)
@click.argument("output", default="./build")
def gen_template(apkg_file, output):
    if apkg_file is None:
        raise Exception("Must apkg_file apkg file")
    if not os.path.exists(output):
        os.mkdir(output)
    apkg = Apkg(apkg_file)
    anki2_structure = apkg.get_anki2()
    anki2_structure.dump_cards_model(output)
    pass


@click.command()
@click.argument("workdir", default=None)
def export(workdir):
    print(workdir)
    pass


command.add_command(gen_template)
command.add_command(export)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    command()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
