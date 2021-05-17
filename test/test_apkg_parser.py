import os
import unittest

import mdformat

from anki_converter.anki2 import Apkg, Render


class TestApkgParser(unittest.TestCase):
    def setUp(self) -> None:
        test_file = "./English_Grammar_In_Use_Exercises.apkg"
        self.output = './resource/test_apkg'
        self.apkg = Apkg(test_file, output=self.output)
        self.anki2_structure = self.apkg.get_anki2()

        pass

    def test_parse_apkg_file(self):
        self.assertIsNotNone(self.anki2_structure)

    def test_dump_model_template(self):
        self.anki2_structure.dump_cards_model(self.output)

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

                # Input filepath as a string...
            # mdformat.file(deck_file)

            pass
