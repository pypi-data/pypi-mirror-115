from typing import List, Dict, Tuple

from miniut import config as cfg
from miniut import console


# key: id, group of report
# value: a list of tuples of 2 values:
#        the first value is a title and the second value is a description
_report: Dict[str, List[Tuple[str, str]]] = {}


_report_titles: Dict[str, int] = {}
_max_id_len: int = 0


_GENERAL_REPORT_LANG = {cfg.ENG : 'Total of < {id} > with erros {tab} : {n_errors}',
                        cfg.ESP : 'Total de < {id} > con errores {tab} : {n_errors}',
                        }

_BLOCK_LANG_GENERAL = {cfg.ENG : 'General report',
                       cfg.ESP : 'Reporte general'
                       }

_BLOCK_LANG_DETAIL = {cfg.ENG : 'Detail report',
                      cfg.ESP : 'Reporte detallado'
                      }


def add_id(id: str):
    global __informe, _max_id_len
    if id not in _report:
        _report[id] = []
        _max_id_len = max(_max_id_len, len(id))


def add_message_by_id(id: str, title: str, message: str = ''):
    add_id(id)
    _report[id].append((title, message))
    
    global _report_titles
    if id not in _report_titles:
        _report_titles[id] = 0
    _report_titles[id] = max(_report_titles[id], len(title))


def ge_val_per_id(id: str) -> list:
    return _report[id]


def num_total_values() -> int:
    n = 0
    for id in _report:
        n += num_errors_by_id(id)
    return n


def num_errors_by_id(id: str) -> int:
    try:    n = len(ge_val_per_id(id=id))
    except: n = 0
    return  n


@console.block(message_block=_BLOCK_LANG_GENERAL)
def print_general_report():
    for id in _report:
        n_errors = num_errors_by_id(id)
        color = console.RED if n_errors > 0 else console.GREEN
        tab = '.' * (_max_id_len - len(id))
        console.println(_GENERAL_REPORT_LANG[cfg.lang()].format(id=id, tab=tab, n_errors=n_errors), color=color)


@console.block(message_block=_BLOCK_LANG_DETAIL)
def print_detail_report():
    for id in _report:
        for title, message in _report[id]:
            console.warning(f'{id} : {title} | {message} ')


def general_report_string() -> str:
    report = ''
    for id in _report:
        n_errors = num_errors_by_id(id)
        tab = '.' * (_max_id_len - len(id))
        report += f'{_GENERAL_REPORT_LANG[cfg.lang()].format(id=id, tab=tab, n_errors=n_errors)}\n'
    return report


def detail_report_string() -> str:
    report = ''
    for id in _report:
        for title, message in _report[id]:
            report += f'{id} : {title} | {message}\n'
    return report
