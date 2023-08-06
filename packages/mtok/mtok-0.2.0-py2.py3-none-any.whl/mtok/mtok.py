"""

    """

import json
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass
class KeyVal :
    key: str
    val: str

def make_raw_github_url(user , repo , branch , fn) :
    return f'https://raw.github.com/{user}/{repo}/{branch}/{fn}'

def make_raw_github_url_with_credentials(user ,
                                         token ,
                                         targ_usr ,
                                         targ_repo ,
                                         branch ,
                                         fn) :
    return f'https://{user}:{token}@raw.githubusercontent.com/{targ_usr}/{targ_repo}/{branch}/{fn}'

def read_json(fp) :
    with open(fp , 'r') as f :
        return json.load(f)

def get_val_by_key_fr_dct(dct , key = None) :
    if key is None and len(dct) > 0 :
        return KeyVal(key = list(dct.keys())[0] , val = list(dct.values())[0])
    return KeyVal(key = key , val = dct[key])

def get_val_by_key_fr_json_file(fp , key = None) :
    js = read_json(fp)
    return get_val_by_key_fr_dct(js , key = key)

def get_local_gtok_fp(github_usr , github_repo , branch , fps_fn , gtok_fn) :
    url = make_raw_github_url(github_usr , github_repo , branch , fps_fn)
    rsp = requests.get(url)
    js = rsp.json()
    for pdir in js.values() :
        fp = Path(pdir) / gtok_fn
        if fp.exists() :
            return fp

def get_all_tokens_fr_private_repo(gtok_fp , github_repo , branch , fn) :
    ur = get_val_by_key_fr_json_file(gtok_fp)
    url = make_raw_github_url_with_credentials(ur.key ,
                                               ur.val ,
                                               ur.key ,
                                               github_repo ,
                                               branch ,
                                               fn)
    rsp = requests.get(url)
    return rsp.json()

def get_token(key_in_all_tokens = None ,
              github_usr = 'imahdimir' ,
              github_repo = 'tok' ,
              branch = 'main' ,
              fps_fn = 'main.json' ,
              gtok_fn = '.gtok.json' ,
              all_tokens_repo = 'tokens' ,
              all_tokens_branch = 'main' ,
              all_tokens_fn = 'main.json') :
    gtok_fp = get_local_gtok_fp(github_usr ,
                                github_repo ,
                                branch ,
                                fps_fn ,
                                gtok_fn)
    if gtok_fp is None :
        return input('Enter token:')
    if (key_in_all_tokens is None) or (key_in_all_tokens == github_usr) :
        return get_val_by_key_fr_json_file(gtok_fp).val
    atoks = get_all_tokens_fr_private_repo(gtok_fp ,
                                           all_tokens_repo ,
                                           all_tokens_branch ,
                                           all_tokens_fn)
    return atoks[key_in_all_tokens]
