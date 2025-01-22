import requests

if __name__ == "__main__":
    text = """# Python

```
print('Привет, мир')
```

/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}

---

# Python

```
a = 2
b = 4
print(a * b)
```

/speech{А здесь представлена другая программа, которая умножается число два на число четыре.}
    """
    r = requests.post("http://127.0.0.1:8000/generate_video", json={'text': text})

    data = r.content
    path = './temp.mp4'
    with open(path, 'wb') as s:
        s.write(data)

