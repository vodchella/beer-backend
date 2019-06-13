from pkg.utils.git import get_top_commit


SERVER_NAME = 'MyBeer REST server'
SERVER_VERSION = '0.01'


def get_software_version_str():
    commit = get_top_commit()
    commit_str = f'.{commit}' if commit else ''
    return '%s v%s%s' % (SERVER_NAME, SERVER_VERSION, commit_str)


SOFTWARE_VERSION = get_software_version_str()
