import json
import os
import tempfile
import shutil
import unittest

from dslibrary.transport.to_local import DSLibraryLocal
from tests.t_utils import reset_env


class TestMMLocal(unittest.TestCase):
    def test_parameters(self):
        tmpdir = tempfile.mkdtemp()
        mm = DSLibraryLocal(tmpdir, spec={"parameters": {"x": "123"}})
        with open(os.path.join(tmpdir, "metadata.json"), 'w') as f_w:
            json.dump({"entry_points": {"main": {"parameters": {"x": {"type": "float"}}}}}, f_w)
        assert mm.get_parameters() == {"x": 123}
        assert mm.get_parameter("x") == 123
        assert mm.get_parameter("y", "Y") == "Y"
        shutil.rmtree(tmpdir)

    def test_metadata(self):
        """
        Metadata can be defined in a specially named file in the model's folder.  It defines such things as entry point
        names, commands to run, and parameter types.
        """
        tmpdir = tempfile.mkdtemp()
        mm = DSLibraryLocal(tmpdir)
        with open(os.path.join(tmpdir, "metadata.json"), 'w') as f_w:
            json.dump({"uri": "x", "entry_points": {"main": {"command": "python run.py", "parameters": {"x": {"type": "string"}}}}}, f_w)
        m = mm.get_metadata()
        assert m.uri == "x"
        assert "main" in m.entry_points
        assert m.entry_points["main"].command == "python run.py"
        assert m.entry_points["main"].parameters["x"].type == "string"
        shutil.rmtree(tmpdir)

    def test_resources(self):
        tmpdir = tempfile.mkdtemp()
        mm = DSLibraryLocal(tmpdir)
        # really simple write/read
        mm.write_resource("f1", "xxx")
        assert mm.read_resource("f1", 'r') == "xxx"
        assert os.path.exists(tmpdir + "/f1")
        shutil.rmtree(tmpdir)

    def tearDown(self) -> None:
        reset_env("test_local")

