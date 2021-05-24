import os
import unittest

import mdformat

from ankdown.anki2 import Apkg, Render, MarkDownCardExporter


class TestApkgParser(unittest.TestCase):
    def setUp(self) -> None:
        cur_dir = os.path.dirname(__file__)
        test_file = os.path.join(cur_dir, "../resource/English_Grammar_In_Use_Exercises.apkg")
        self.output = os.path.join(cur_dir, '../resource/test_apkg')
        self.apkg = Apkg(test_file, output=self.output)
        self.collection = self.apkg.get_anki2()

        pass

    def test_parse_apkg_file(self):
        self.assertIsNotNone(self.collection)

    def test_dump_model_template(self):
        # self.collection.dump_cards_model(self.output)
        pass

    def test_export_cards(self):
        md_exporter = MarkDownCardExporter(self.collection)
        md_exporter.do_export_cards_by_deck('/tmp/')

        pass

    def test_remap_media(self):
        self.apkg.remap_media()
        pass
