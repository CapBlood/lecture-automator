import pytest
from lecture_automator.parser import join_slides, parse_slides, process_commands


def test_join_slides():
    text = (
        "#Markdown Presentation Ecosystem\n"
        "\n"
        "Lin-e\n"
        "/speech{It's a speech}\n"
        "\n"
        "---\n"
        "\n"
        "# Slide\n"
        "Something\n"
        "/speech{Something}"
    )
    slides = [
        (
            "#Markdown Presentation Ecosystem\n"
            "\n"
            "Lin-e\n"
            "/speech{It's a speech}\n"
            "\n"
        ),
        (
            "\n"
            "# Slide\n"
            "Something\n"
            "/speech{Something}"
        )
    ]

    assert join_slides(slides) == text


def test_join_slides_2():
    text = (
        "---\n"
        "theme: gaia\n"
        "_class: lead\n"
        "paginate: true\n"
        "backgroundColor: #fff\n"
        "backgroundImage: url('https://marp.app/assets/hero-background.svg')\n"
        "---\n"
        "\n"
        "# Python\n"
        "\n"
        "```\n"
        "print('Привет, мир')\n"
        "/speech{sdfsdf}\n"
        "```\n"
        "\n"
        "/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}\n"
        "\n"
        "---\n"
        "\n"
        "# Python\n"
        "\n"
        "```\n"
        "a = 2\n"
        "b = 4\n"
        "print(a * b)\n"
        "```\n"
        "\n"
        "/speech{А здесь представлена другая программа, которая умножает число два на число четыре.}\n"
        "\n"
    )
    metaslide = (
        "theme: gaia\n"
        "_class: lead\n"
        "paginate: true\n"
        "backgroundColor: #fff\n"
        "backgroundImage: url('https://marp.app/assets/hero-background.svg')\n"
    )
    slides = [
        (
            "\n"
            "# Python\n"
            "\n"
            "```\n"
            "print('Привет, мир')\n"
            "/speech{sdfsdf}\n"
            "```\n"
            "\n"
            "/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}\n"
            "\n"
        ),
        (
            "\n"
            "# Python\n"
            "\n"
            "```\n"
            "a = 2\n"
            "b = 4\n"
            "print(a * b)\n"
            "```\n"
            "\n"
            "/speech{А здесь представлена другая программа, которая умножает число два на число четыре.}\n"
            "\n"
        )
    ]

    assert join_slides(slides, metaslide=metaslide) == text



def test_parse_slides():
    text = (
        "---\n"
        "theme: gaia\n"
        "_class: lead\n"
        "paginate: true\n"
        "backgroundColor: #fff\n"
        "backgroundImage: url('https://marp.app/assets/hero-background.svg')\n"
        "---\n"
        "\n"
        "# Python\n"
        "\n"
        "```\n"
        "print('Привет, мир')\n"
        "/speech{sdfsdf}\n"
        "```\n"
        "\n"
        "/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}\n"
        "\n"
        "---\n"
        "\n"
        "# Python\n"
        "\n"
        "```\n"
        "a = 2\n"
        "b = 4\n"
        "print(a * b)\n"
        "```\n"
        "\n"
        "/speech{А здесь представлена другая программа, которая умножает число два на число четыре.}\n"
        "\n"
    )
    expected_slides = [
        (
            "\n"
            "# Python\n"
            "\n"
            "```\n"
            "print('Привет, мир')\n"
            "/speech{sdfsdf}\n"
            "```\n"
            "\n"
            "/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}\n"
            "\n"
        ),
        (
            "\n"
            "# Python\n"
            "\n"
            "```\n"
            "a = 2\n"
            "b = 4\n"
            "print(a * b)\n"
            "```\n"
            "\n"
            "/speech{А здесь представлена другая программа, которая умножает число два на число четыре.}\n"
            "\n"
        )
    ]
    expected_metaslide = (
        "theme: gaia\n"
        "_class: lead\n"
        "paginate: true\n"
        "backgroundColor: #fff\n"
        "backgroundImage: url('https://marp.app/assets/hero-background.svg')\n"
    )

    metaslide, slides = parse_slides(text)

    assert slides == expected_slides
    assert metaslide == expected_metaslide


def test_parse_slides_2():
    text = (
        "#Markdown Presentation Ecosystem\n"
        "\n"
        "Lin-e\n"
        "/speech{It's a speech}\n"
        "\n"
        "---\n"
        "\n"
        "# Slide\n"
        "Something\n"
        "/speech{Something}"
    )
    expected_slides = [
        (
            "#Markdown Presentation Ecosystem\n"
            "\n"
            "Lin-e\n"
            "/speech{It's a speech}\n"
            "\n"
        ),
        (
            "\n"
            "# Slide\n"
            "Something\n"
            "/speech{Something}"
        )
    ]
    expected_metaslide = None

    metaslide, slides = parse_slides(text)

    assert slides == expected_slides
    assert metaslide == expected_metaslide


def test_process_commands():
    slides = [
        (
            "#Markdown Presentation Ecosystem\n"
            "\n"
            "Lin-e\n"
            "/speech{It's a speech}\n"
            "\n"
        ),
        (
            "\n"
            "# Slide\n"
            "Something\n"
            "/speech{Something}"
        )
    ]
    expected_slides = [
        (
            "#Markdown Presentation Ecosystem\n"
            "\n"
            "Lin-e\n"
            "\n"
            "\n"
        ),
        (
            "\n"
            "# Slide\n"
            "Something\n"
        )
    ]
    expected_metadata = {
        1: {
            'speech': "It's a speech"
        },
        2: {
            'speech': "Something"
        }
    }

    processed_slides, metadata = process_commands(slides)

    assert expected_slides == processed_slides
    assert expected_metadata == metadata

def test_process_commands_2():
    slides = [
        (
            "#Markdown Presentation Ecosystem\n"
            "\n"
            "Lin-e\n"
            "\n"
            "\n"
        ),
        (
            "\n"
            "# Slide\n"
            "Something\n"
            "/speech{Something}"
        )
    ]

    with pytest.raises(Exception):
        processed_slides, metadata = process_commands(slides)

