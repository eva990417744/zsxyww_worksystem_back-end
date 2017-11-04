from qiniu import *

ak = 'eT9_3M_aVAPgnV6fiInoSPUsN8IEgOaYDizm1svP'
sk = 'T0xt-IpK6itieVBXblcVWUwKu_Iw0hT2tzKZT2M1'

def get_qiniu_token():
    policy = {
        'scope': '<bucket>',
        'callbackUrl': 'http://work.zsxyww.com/work/qiniu_callback/',
        'callbackBody': 'id=$(x:id),tname=$(x:tname)',
        'callbackFetchKey': 1,
        'fsizeMin': 1,
        'mimeLimit': 'image/*',
    }
    q = Auth(access_key=ak, secret_key=sk)
    return q.upload_token('zsxyww-work-oredr-image',policy=policy)


