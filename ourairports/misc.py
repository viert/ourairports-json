from subprocess import check_output

GIT_BINARY = "/usr/bin/git"


def repo_changed() -> bool:
    output = check_output([GIT_BINARY, "status", "-z"])
    return output.strip() != ""
