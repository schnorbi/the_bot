import configparser
config = configparser.ConfigParser()


def configreader(part):
    config.read('npod_conf.txt')
    if part == 'nasa':
        return config.get('API-Keys', 'nasa_api_key')
    elif part == 'discord':
        return config.get('API-Keys', 'discord_api_key')
    elif part == 'owner':
        return config.get('Discord-Bot', 'owner')
    elif part == 'nasa_pod_channels':
        return config.get('NASA-POD', 'channels')