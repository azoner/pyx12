import gc
import importlib
import os
import tempfile
import unittest
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import pyx12.errh_xml


class TempFileLifetime(unittest.TestCase):
    def test_temp_file_removed_when_handler_is_collected(self):
        eh = pyx12.errh_xml.err_handler()
        path = eh.getFilename()
        eh.handleErrors([("ele", "1", "Name too long", "SMITH", 3)])
        eh.Write(3)
        eh.close()
        self.assertTrue(os.path.exists(path))
        del eh
        gc.collect()
        self.assertFalse(os.path.exists(path))

    def test_explicit_output_path_is_kept(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "errors.xml")
            with pyx12.errh_xml.err_handler(xml_out=path) as eh:
                eh.Write(1)
            del eh
            gc.collect()
            self.assertTrue(os.path.exists(path))


class Deprecation(unittest.TestCase):
    def test_import_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(pyx12.errh_xml)
        messages = [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]
        self.assertTrue(any("removed in 5.0" in m for m in messages), messages)
