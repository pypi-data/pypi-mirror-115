import zipfile
from shutil import copytree

import wget


def copy_template(name, template_name, temp_path, verbose=False):
    if verbose:
        print("creating project {}".format(name))
    src_path = "{}/tmp/bouto-main/templates/{}".format(
        temp_path, template_name
    )
    dest_path = "./{}".format(name)
    copytree(src_path, dest_path)


def download(url, temp_path, verbose=False):
    if verbose:
        print("downloading from {} to tmp.zip".format(url))
    wget.download(url, "{}/tmp.zip".format(temp_path))


def unzip(temp_path, verbose=False):
    zip_path = "{}/tmp.zip".format(temp_path)
    extract_path = "{}/tmp/".format(temp_path)
    if verbose:
        print("extracting {} to {}".format(zip_path, extract_path))
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
