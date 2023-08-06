`parse_m3u8(io)`

io : IO对象`io.FileIO, io.StringIO, io.BytesIO`等

返回一个生成器

每次返回一个解析到的`url: str`

使用例子:

~~~python
from syllib.m3u8 import parse_m3u8

with open('filename', 'r') as f:
    for url in parse_m3u8(f):
        do(url)  # do something
~~~