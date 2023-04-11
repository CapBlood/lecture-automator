import re


def preprocess_md_marp(text: str) -> str:
    """Предобработка текста Markdown перед использованием в Marp. Производит удаление
    управляющих команд (/speech и т.п.).

    Args:
        text (str): текст для предобработки.

    Returns:
        str: предобработанный текст.
    """

    text = re.sub(r'/[a-z]+ *\{[^\{\}]+\}', '', text)
    return text


def parse_speech(text: str) -> dict:
    """Парсинг речи для каждого слайда в презентации Markdown.

    Args:
        text (str): текст Markdown.

    Returns:
        dict: словарь с метаданными слайдов (речи для каждого из слайдов) вида `{1: 'Первая речь', 2: 'Вторая речь'}` (нумерация слайдов с 1).
    """

    text = re.sub(r'(?m)\`{3}[^\`]+\`{3}', '', text)
    slides = re.split(r'(?m)^\-{3}\n', text)

    speeches = list()
    for slide in slides:
        r = re.findall(r'/speech *\{([А-Яа-яA-Za-z \S]+)\}', slide)

        if len(r) == 0:
            raise Exception(
                'Каждый слайд должен иметь описание речи слайда!'
            )
        if len(r) > 1:
            raise Exception(
                'Каждый слайд должен иметь только одно описание речи слайда!'
            )
        speeches.append(r[0])

    return speeches



def parse_md(path: str) -> dict:
    """Парсинг Markdown презентации формата Marp с дополнительными управляющими командами (/speech и т.д.)

    Args:
        path (str): путь к файлу Markdown.

    Returns:
        dict: словарь, содержащий текст Markdown для Marp (с удаленными управляющими командами) и метаданные.
    """

    with open(path) as file:
        md_text = file.read()

    preprocessed_marp_text = preprocess_md_marp(md_text)
    speech_metadata = parse_speech(md_text)

    return {
        'md_text': preprocessed_marp_text,
        'speech': speech_metadata
    }

    
if __name__ == '__main__':
    res = parse_md("examples/Example.md")
    # print(res['md_text'])
    print(res['speech'])