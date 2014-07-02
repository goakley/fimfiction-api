import configparser


def load_configuration(file_object):
    """
    Returns the (username, password) from the passed configuration file
    """
    parser = configparser.ConfigParser()
    config = parser.read_file(file_object)
    username = config.get('user', 'username')
    password = config.get('user', 'password')
    return (username, password)
