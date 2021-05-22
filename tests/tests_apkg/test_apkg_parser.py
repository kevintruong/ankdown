import os
import unittest

import mdformat

from ankdown.anki2 import Apkg, Render


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
        render = Render(work_dir=self.output,
                        includes=['/home/kevin/Project/Memflask/anki_convertor/macros'])
        for each_deck, deck in self.anki2_structure.cards_by_decks:
            deck_name = f'{deck.deck_name.values[0]}.md'
            deck_file = os.path.join(self.output, deck_name)
            with open(deck_file, 'w') as deck_file_fd:
                for card in deck.iterrows():
                    card_content = render.export_card(card)
                    print(card_content)
                    deck_file_fd.write("\r\n" + card_content)

    def test_remap_media(self):
        self.apkg.remap_media()
        pass
