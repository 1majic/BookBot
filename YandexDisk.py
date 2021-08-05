import yadisk

y = yadisk.YaDisk(token="")


def uploadFile(file, path):
    y.upload(file, path)


def downloadFile(path):
    y.download(path, path[path.rindex("/")+1:])


def getBooks():
    return [i.name for i in y.listdir("books/books")]

