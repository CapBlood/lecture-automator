import click

from lecture_automator.compiler import compile_text_md


@click.command()
@click.argument(
    'input_md',
    type=click.STRING,
)
@click.argument(
    'out_path',
    type=click.STRING,
)
@click.option(
    '--vformat',
    type=click.Choice(['mp4', 'webm']),
    default='mp4',
    help=(
        'Формат генерируемого видео.'
    )
)
@click.option(
    '--scale',
    type=click.FLOAT,
    default=1.5,
    help=(
        'Коэффициент масштабирования генерируемого видео, '
        'по умолчанию равен 1.5, что соответствует разрешению 1920x1080,'
        'значение 1 соответствует разрешению 1280x720.'
    )
)
def convert_md_to_mp4(input_md, out_path, scale, vformat):
    with open(input_md) as file:
        md_text = file.read()

    compile_text_md(
        md_text, out_path=out_path,
        vformat=vformat, scale=scale
    )


if __name__ == '__main__':
    convert_md_to_mp4()
