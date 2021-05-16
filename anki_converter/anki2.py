import json
import os
import sqlite3
import tempfile
from collections import OrderedDict
from pathlib import Path
from typing import Union
from zipfile import ZipFile
from markdownify import markdownify as md

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from anki_converter import i18n


class Anki2:
    """Reads the original *.anki2 SQLite database

    Mutates the database to make it easier to read.
    """

    def __init__(self, filename: Union[str, Path], **kwargs):
        con = sqlite3.connect(str(filename))
        decks = pd.read_sql_query("SELECT decks FROM col", con)
        decks = json.loads(decks.values[0][0])
        col = pd.read_sql_query("SELECT models FROM col", con)
        self.model = json.loads(col.values[0][0])
        for model_id, model_cfg in self.model.items():
            if not hasattr(model_cfg, 'fields'):
                model_cfg['fields'] = []
            for each_column in model_cfg['flds']:
                model_cfg['fields'].append(each_column['name'])
        cards = pd.read_sql_query("""SELECT c.id,c.nid,c.did,n.mid,n.flds from cards c join notes n on c.nid = n.id """,
                                  con)
        cards['flds'] = cards.apply(lambda row: OrderedDict(zip(self.model[str(row.mid)]['fields'],
                                                                row.flds.split('\x1f'))), axis=1)

        cards['deck_name'] = cards.apply(lambda row: decks[str(row.did)]['name'], axis=1)
        cards['model'] = cards.apply(lambda row: self.model[str(row.mid)]['fields'], axis=1)
        self.cards_by_decks = cards.groupby(cards.did)

    def dump_cards_model(self, output):

        def dump_example_card_record():
            return i18n.t("info.template.comment")

        def dump_example():
            return i18n.t("info.template.example")

        for each_model, model_conf in self.model.items():
            with open(os.path.join(output, f"{each_model}.jinja2"), 'w') as template_file:
                content = ""
                content += dump_example()
                content += dump_example_card_record()
                for each_field in model_conf['fields']:
                    content += f"{{{{ {each_field} }}}}\r\n"
                template_file.write(content)
                # frontmatter.dump(content, template_file)
                # example records for a cards


class Render:
    def __init__(self, work_dir, **kwargs):
        self.work_dir = work_dir
        self.includes = kwargs.get('includes', [])
        self.anki2 = Anki2(os.path.join(work_dir, "anki2/collection.anki2"))
        self.env = Environment(loader=FileSystemLoader([work_dir] + self.includes))
        self.templates = self.load_template()

    def load_template(self):
        templates = {}
        for each_model, model_conf in self.anki2.model.items():
            model_template_file = f"{each_model}.jinja2"
            if os.path.isfile(os.path.join(self.work_dir, model_template_file)):
                templates[each_model] = self.env.get_template(model_template_file)
        return templates

    def export(self, type='markdown'):
        if type == 'markdown':
            return self.markdown_export()
        pass

    def export_card(self, card):
        mid = card[1]['mid']
        card_data = card[1]['flds']

        for key in card_data.keys():
            card_data[key] = md(card_data[key])
            if key == "Choices":
                card_data[key] = card_data[key].split("/")
        # card_data = {x:md(card_data[x]) for (x,_) in card_data.items()}
        print(card_data)
        ret = ""
        template = self.templates.get(str(f'{card[1]["mid"]}'), None)
        if template:
            ret = template.render(card_data).lstrip().rstrip()
        return ret

    def markdown_export(self):
        for each_cards in self.anki2.cards_by_decks:
            card = self.export_card(each_cards)
            pass
        pass


class Apkg:
    """Reads a *.apkg file"""

    original: Path
    folder: Path
    media_path: Path

    def __init__(self, filename_or_dir: Union[str, Path], **kwargs):
        """
        ```python
        from ankisync2.apkg import Apkg, db

        apkg = Apkg("example.apkg")
        # Or Apkg("example/") also works. the folder named 'example' will be created.
        ```

        Args:
            filename_or_dir (Union[str, Path]): Can be a *.apkg, or a folder name
        """
        self.output = kwargs.get('output', tempfile.mkdtemp())
        self.output = Path(self.output)
        self.anki2 = self.output.joinpath('anki2')
        os.makedirs(self.output, exist_ok=True)
        self.original = Path(filename_or_dir)
        if not self.original.is_dir():
            self.folder = self.original.with_suffix("")
            self._unzip()
        else:
            self.folder = self.original
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        self.media_path = self.folder.joinpath("media")
        if not self.media_path.exists():
            self.media_path.write_text("{}")

        # shutil.copy(
        #     self.folder.joinpath("collection.anki2"),
        #     self.folder.joinpath("collection.anki20"),
        # )
        # super().__init__(self.folder.joinpath("collection.anki20"), **kwargs)

    def _unzip(self):
        if self.output.exists():
            with ZipFile(self.original) as zf:
                zf.extractall(os.path.join(self.output, "anki2"))

    def get_anki2(self):
        return Anki2(self.anki2.joinpath("collection.anki2"))

    def markdown_dump(self, anki2_collection):
        anki2_collection: Anki2
        dump_dir = os.path.join(self.folder, "md_dump")
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        for each_deck, cards_deck in anki2_collection.cards_by_decks:
            for each_card in cards_deck:
                deck_file = os.path.join(dump_dir, f"{cards_deck.name}.md")
