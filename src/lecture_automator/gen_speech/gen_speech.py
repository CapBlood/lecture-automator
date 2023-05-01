# -*- coding: utf-8 -*-

import os
import tempfile

import torch
from lecture_automator.gen_speech.utils import concat_wavs, divide_text

from lecture_automator.settings import get_app_dir


MODEL_URL = 'https://models.silero.ai/models/tts/ru/v3_1_ru.pt'
MODEL_FILENAME = 'v3_1_ru.pt'
SPEAKER = 'xenia'
SAMPLE_RATE = 48000
MAX_SYMBOLS = 1000


def generate_speech(model, text: str, out_path: str, device: str = 'cpu') -> str:
    """Синтез речи.

    Args:
        model (_type_): модель для синтеза речи.
        text (str): текст для синтеза речи.
        out_path (str): полный путь к файлу для сохранения синтезированной речи.
        device (str, optional): устройство для вычислений модели. Defaults to 'cpu'.

    Returns:
        str: путь к синтезированной речи.
    """
    
    model.to(device)

    curr_dir = os.getcwd()
    os.chdir(os.path.dirname(out_path))
    audio_path = model.save_wav(
        text=text,
        speaker=SPEAKER,
        sample_rate=SAMPLE_RATE
    )
    os.rename(audio_path, os.path.basename(out_path))
    os.chdir(curr_dir)

    return out_path


def get_model(model_name: str):
    """Загрузка модели.

    Args:
        model_name (str): название модели для загрузки.

    Returns:
        _type_: _description_
    """

    model_path = os.path.join(get_app_dir(), model_name)

    if not os.path.exists(model_path):
        torch.hub.download_url_to_file(
            MODEL_URL,
            model_path
        )

    model = torch.package.PackageImporter(model_path).load_pickle(
        "tts_models", "model"
    )

    return model


def text_to_speech(text: str, out_path: str, device: str = 'cpu') -> str:
    """Синтез речи.

    Args:
        text (str): текст для синтеза речи.
        out_path (str): путь для сохранения сгенерированной речи.
        device (str, optional): устройство для вычислений (cuda, cpu и т.д.). Defaults to 'cpu'.

    Returns:
        str: название файла формата wav со сгенерированной речью по тексту.
    """

    model = get_model(MODEL_FILENAME)

    if len(text) > MAX_SYMBOLS:
        texts = divide_text(text, max_length=MAX_SYMBOLS)
    else:
        texts = [text]

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_wavs = []
        for i, t in enumerate(texts):
            temp_out_path = os.path.join(tmpdirname, 'speech_{}'.format(str(i)))
            generate_speech(model, t, temp_out_path)
            temp_wavs.append(temp_out_path)
        concat_wavs(temp_wavs, out_path)
        
    return out_path


def texts_to_speeches(texts: list, out_dir: str, basename: str = 'Sound') -> list:
    audio_paths = []
    for index, text in enumerate(texts, start=1):
        audio_path = os.path.join(out_dir, '{}_{}.wav'.format(basename, index))
        text_to_speech(
            text, audio_path
        )
        audio_paths.append(audio_path)

    return audio_paths


if __name__ == '__main__':
    # text_to_speech('Зачем ты запустил код?', "./example.wav")
    # audio_paths = texts_to_speeches(['Привет', 'Пока'], '.')
    # print(audio_paths)
    text = 'Рассмотрим пример с использованием ООП. Допустим мы хотим написать программу для подсчета яблок в корзинке. Что нам для этого нужно? Очевидно, что нам нужна корзинка, которая будет иметь некоторое количество яблок. Для программной имитации корзинки мы напишем класс, который будет описывать корзинку, а именно нам интересна только одна из характеристик корзинки, то есть количество яблок в ней. Давайте рассмотрим код. Класс в Пайтоне определяется с помощью ключевого слова "класс", после которого следует название класса, а после название класса следует двоеточие. В самом классе мы определим специальный метод-инициализатор "инит", в котором создаются поля данных класса или характеристики, как уже было сказано нас интересует количество яблок, поэтому мы создали в этом методе поле "нум эпл" и инициализировали его нулем, так как в начале наша корзинка будет содержать ноль яблок. Также необходимо обратить внимание на аргумент функции под названием "сэлф", он используется для получение значения поля или для записи нового значения в поле. Также в классе мы определили два метода: "мефат один" и "мефат два". Первый метод добавляет добавляет в корзинку одно яблоко, а второй достает из него одно яблоко. Вот таким образом мы и описали нашу будущую корзинку: её свойства или характеристики и функциональность. Теперь используя этот класс мы можем создавать объекты, то есть сами корзинки, класс же служит лишь их описанием. Далее мы используем этот класс, чтобы создать корзинку, вызывая имя класса как функцию. Обратите внимание, что в скобках пусто, мы не передаем никакие аргументы, это связано с тем, что "сэлф" передавать не нужно, а если же кроме "сэлф" будут другие аргументы, то уже будет необходимо их указывать. Затем мы выводим количество текущих яблок в созданной корзине, получая к ним доступ через созданный объект и точку, и получаем в выводе ноль. Затем добавляем с помощью метода одно яблоко и снова выводим - получаем одно яблоко в корзине.'
    text_to_speech(text, './examples/test.wav')
    
    # res = divide_text(text)
    # print(res)