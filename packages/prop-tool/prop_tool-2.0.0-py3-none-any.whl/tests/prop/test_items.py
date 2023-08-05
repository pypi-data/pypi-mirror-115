"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.config.config import Config
from proptool.prop.items import Blank, Comment, PropItem, Translation
from tests.test_case import TestCase


class TestPropItem(TestCase):

    def test_base_constructor_args_none(self) -> None:
        item = PropItem()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_base_constructor_args(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        item = PropItem(value, key)
        self.assertEqual(key, item.key)
        self.assertEqual(value, item.value)

    def test_base_to_string_not_implemented(self) -> None:
        item = PropItem()
        with self.assertRaises(NotImplementedError):
            item.to_string()

    # #################################################################################################

    def test_translation_invalid_key_type(self) -> None:
        """
        Tests handing of invalid key type.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(123, value)
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(None, value)

    def test_translation_empty_key(self) -> None:
        """
        Tests handling of empty key.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation('', value)

    def test_translation_empty_key_after_strip(self) -> None:
        """
        Tests handling of non-empty key that gets empty once strip()'ed.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation('   ', value)

    def test_translation_invalid_value_type(self) -> None:
        with self.assertRaises(ValueError):
            key = self.get_random_string()
            # noinspection PyTypeChecker
            Translation(key, 1234)

        value = self.get_random_string()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(key, value, None)

    def test_translation_invalid_separator(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation(key, value, '-')

    def test_translation_empty_separator(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation(key, value, '')

    def test_translation_to_string(self) -> None:
        config = Config()
        for separator in config.ALLOWED_SEPARATORS:
            key = self.get_random_string()
            value = self.get_random_string()
            trans = Translation(key, value, separator)
            expected = f'{key} {separator} {value}'
            self.assertEqual(expected, trans.to_string())

    # #################################################################################################

    def test_comment_constructor(self) -> None:
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            item = Comment(value)
            self.assertEqual(value, item.value)
            self.assertIsNone(item.key)

    def test_comment_invalid_value(self) -> None:
        with self.assertRaises(ValueError):
            # Invalid value type
            # noinspection PyTypeChecker
            Comment(1234)

    def test_comment_without_marker(self) -> None:
        """
        Checks if constructing Comment without valid marker in passed value
        would automatically add such marker.
        """
        val = self.get_random_string('no_maker_')
        # No valid comment marker
        comment = Comment(val)
        self.assertEqual(f'{Config.ALLOWED_COMMENT_MARKERS[0]} {val}', comment.to_string())

    def test_comment_empty_value(self) -> None:
        comment = Comment('')
        self.assertEqual(Config.ALLOWED_COMMENT_MARKERS[0], comment.to_string())

    def test_comment_to_string(self) -> None:
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            comment = Comment(value)
            self.assertEqual(value, comment.to_string())

    # #################################################################################################

    def test_blank_constructor(self) -> None:
        item = Blank()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_blank_to_string(self) -> None:
        item = Blank()
        self.assertEqual('', item.to_string())
