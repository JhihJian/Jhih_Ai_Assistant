import urllib.request

git_doc_url = "https://jhihjian.github.io/JhihJian-Know-Library/"


def git_doc_is_online():
    try:
        contents = urllib.request.urlopen(git_doc_url).read()
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    print(git_doc_is_online())
