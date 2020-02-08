import unittest

from gabtag.music_manager.audio_extension_handler import AudioExtensionHandler


def test_class_audio_extension_handler_has_four_abstract_methods():
    # then
    assert 'get_tag' in AudioExtensionHandler.__abstractmethods__
