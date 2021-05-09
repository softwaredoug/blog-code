import requests
import os
import tarfile


def explode_tgz(filepath, dest='data/'):
    tar = tarfile.open(filepath, 'r')
    for member in tar.getmembers():
        print(f"Extracting {member.name} to {dest}")

    tar.extractall(path=dest)
    tar.close()


def download_one(uri, dest='data/', force=False):
    if not os.path.exists(dest):
        os.makedirs(dest)

    if not os.path.isdir(dest):
        raise ValueError("dest {} is not a directory".format(dest))

    filename = os.path.basename(uri)
    ext = os.path.splitext(filename)
    filepath = os.path.join(dest, filename)
    if os.path.exists(filepath):
        if not force:
            print(filepath + ' already exists')
            return
        print("exists but force=True, Downloading anyway")

    with open(filepath, 'wb') as out:
        print('GET {}'.format(uri))
        resp = requests.get(uri, stream=True)
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)

    if len(ext) > 1:
        ext = ext[1]
        if ext == '.tgz' or ext == '.tar.gz' or ext == '.tar':
            explode_tgz(filepath, dest=dest)


def download(uris, dest='data/', force=False):
    for uri in uris:
        download_one(uri=uri, dest=dest, force=force)
