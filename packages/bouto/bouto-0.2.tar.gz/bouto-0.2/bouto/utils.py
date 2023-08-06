import zipfile
from shutil import copytree

import sys
import wget

def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  # Don't use print() as it will print in new line every time.
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

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
    wget.download(url, "{}/tmp.zip".format(temp_path), bar=bar_progress)


def unzip(temp_path, verbose=False):
    zip_path = "{}/tmp.zip".format(temp_path)
    extract_path = "{}/tmp/".format(temp_path)
    if verbose:
        print("extracting {} to {}".format(zip_path, extract_path))
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
