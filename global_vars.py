import logging
import configparser

logging.basicConfig(level=logging.DEBUG, format='[Star] %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def init():
    global gol_dict
    gol_dict = {}


def get_var(key):
    try:
        var = gol_dict[key]
        return var
    except KeyError as e:
        log.debug('获取变量失败，变量可能不存在')


def set_var():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    sections = []
    options = []
    for section in cfg.sections():
        sections.append(section)
    for section in sections:
        for option in cfg.options(section):
            options.append((section, option))
    for option_value in options:
        gol_dict[option_value[1]] = cfg.get(option_value[0], option_value[1])
    return gol_dict


init()
set_var()
