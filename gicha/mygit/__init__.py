from git import Repo, Git, rmtree
from tempfile import mkdtemp


def checkout(url, tag, no_git=True):
    tmp_dir = mkdtemp()

    Repo.clone_from(url, tmp_dir)
    repo = Git(tmp_dir)
    repo.checkout(tag)
    if no_git:
        rmtree(tmp_dir + "/.git")

    return tmp_dir
