import os

import pytest
from lecture_automator.marp_api import generate_marp_slides

pytest_plugins = ["pytester"]


def test_generate_marp(tmpdir):
    md_text = (
        "# Markdown Presentation Ecosystem"
        "This is text."
        "\n"
        "---"
        "\n"
        "Slide"
        "Something"
    )

    generate_marp_slides(tmpdir, md_text)
    assert len(os.listdir(tmpdir)) == 2
