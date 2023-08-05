def read(fileName,encoding="utf-8"):
    with open(fileName,"r",encoding=encoding) as f:
        return f.read()
def write(fileName,text="",encoding="utf-8"):
    with open(fileName,"w",encoding=encoding) as f:
        f.write(text)
def add(fileName,text="",encoding="utf-8"):
    with open(fileName,"a",encoding=encoding) as f:
        f.write(text)
