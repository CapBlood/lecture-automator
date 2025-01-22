import os
import subprocess

from fastapi import FastAPI, Response
from pydantic import BaseModel

from lecture_automator.compiler import compile_text_md
from lecture_automator.settings import get_cache_dir
from lecture_automator.marp_api.exceptions import MarpError


class MarpText(BaseModel):
    text: str


app = FastAPI()


@app.post("/generate_video")
async def generate_video(data: MarpText):
    storage_path = get_cache_dir()

    try:
        out_path = os.path.join(storage_path, 'Video.webm')
        compile_text_md(
            data.text, out_path=out_path)
    except MarpError as e:
        print('error')
        print(e.stderr)
        print(e.stdout)
        return

    with open(out_path, 'rb') as file:
        video_data = file.read()

    return Response(content=video_data, media_type="video/mp4")
