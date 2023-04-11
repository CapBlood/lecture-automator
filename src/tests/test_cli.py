import os

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def run(testdir):
    def do_run(*args):
        args = ["lecture-automator"] + list(args)
        return testdir.run(*args)

    return do_run


def test_cli_exist(tmpdir, run):
    md_text = (
        "# Python"
        "```"
        "print('Привет, мир')"
        "```"
        "/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}"
        "\n"
        "---"
        "\n"
        "# Python"
        "```"
        "a = 2"
        "b = 4"
        "print(a * b)"
        "```"
        "/speech{А здесь представлена другая программа, которая умножается число два на число четыре.}"
    )

    md_path = os.path.join(tmpdir, 'Example.md')
    with open(md_path, 'w') as file:
        file.write(md_text)

    mp4_path = os.path.join(tmpdir, 'Example.mp4')
    result = run(md_path, mp4_path)
    assert result.ret == 0

