import unittest
import subprocess
import shlex
from textwrap import dedent
import json
import shutil


@unittest.skipIf(shutil.which("pandoc") is None, "Pandoc executable not found")
class TestMacro(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_macro(self):
        command = "pandoc --filter panipa --to json"

        data_in = dedent("""
        [tEst]{.xsampa}
        """)

        expected = {
            "pandoc-api-version": [1,22,1],
            "meta": {},
            "blocks": [
                {
                    "t": "Para",
                    "c": [
                        {
                            "t":"Span",
                            "c": [
                                [
                                    "",
                                    ["xsampa"],
                                    []
                                ],
                                [
                                    {
                                        "t": "Str",
                                        "c": "tɛst"
                                    }
                                ]
                            ]
                        }
                    ]
                }
            ]
        }


        pandoc = subprocess.run(shlex.split(command), text=True, input=data_in, stdout=subprocess.PIPE)
        data_out = json.loads(pandoc.stdout.rstrip())
        self.assertEqual(data_out, expected)
