from lecture_automator.parser import parse_speech, preprocess_md_marp


def test_parse_speech():
    text = (
        "#Markdown Presentation Ecosystem"
        "\n"
        "Lin-e"
        "/speech{It's a speech}"
        "\n"
        "---"
        "\n"
        "# Slide"
        "Something"
        "/speech{Something}"
    )

    expected_metadata = [
        "It's a speech",
        'Something'
    ]

    metadata = parse_speech(text)

    assert expected_metadata == metadata


def test_preprocess_md_marp():
    text = """#Markdown Presentation Ecosystem
    
    Lin-e
    
    /speech{It's a speech}
    
    ---
    
    # Slide
    
    Something
    """
    expected_preprocessed = """#Markdown Presentation Ecosystem
    
    Lin-e
    
    
    
    ---
    
    # Slide
    
    Something
    """

    preprocessed_md_marp = preprocess_md_marp(text)

    assert preprocessed_md_marp == expected_preprocessed
