import requests
import json
import time
import pymysql
import random

pgnum = 1
createtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
conn = pymysql.Connect('192.168.1.232','python','python','python',3306)
cur = conn.cursor()
mydic = {
    '门派':('equip_type',10),
    '等级':('equip_level',10),
    '价格': ('price', 10),
    '装评': ('equ_xiuwei', 10),
    '炼护': ('lian_hu', 10),
    '加护': ('jiahu', 10),
    '大法': ('mattack_max', 10),
    '小法': ('mattack_min', 10),
    '大物': ('pattack_max', 10),
    '小物': ('pattack_min', 10),
    '疾语': ('castspeed', 10),
    '追电': ('movespeed', 10),
    '防御': ('pdef', 10),
    '回避': ('avoid', 10),
    '物防': ('mdef', 10),
    '命中': ('hit', 10),
    '会心': ('huixin', 10),
    '万钧': ('wan_jun', 10),
    '御心': ('yu_xin', 10),
    '诛心': ('zhu_xin', 10),
    '名称' : ('equip_name', 20),
}

mytype ={
    '1' : '荒火',
    '2' : '天机',
    '3' : '翎羽',
    '4' : '魍魉',
    '5' : '太虚',
    '6' :  '云麓',
    '7' :  '冰心',
    '8' : '弈剑',
    '9' : '鬼墨',
    '10' : '龙巫',
    '11' : '幽篁',
}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    'Connection': 'keep-alive',
}


while True:
    data = {
        'act': 'overall_search_role',
        'order_by': '',
        'page': pgnum,
        'other_arg': '',
        'price_max': '2000000',
        'price_min': '100000',
        'equip_jia_hu_min': '234',
        'equip_level_min': '80',
        # 'mattack_max':'4000',
    }

    tx3url = 'https://tx3.cbg.163.com/cgi-bin/search.py'
    res = requests.post(tx3url, data=data, headers=headers).content.decode()
    # for k,v in mydic.items():
    #     print('{:<{}s}'.format(k,v[1]-2),end='')
    # print()

    result = json.loads(res)
    for line in result['msg']:
        lineitems = []
        for value in mydic.values():
            if value[0] == 'equip_type':
                lineitems.append(mytype.get(line[value[0]]))
                # print(mytype.get(line[value[0]]))
                # print('{:<{}s}'.format(mytype.get(line[value[0]]), value[1]-2), end='')
            elif value[0] == 'price':
                lineitems.append(str(line[value[0]]/100))
                # print('{:<{}d}'.format(int(line[value[0]]/100), value[1]), end='')
            else:
                lineitems.append(str(line[value[0]]))
                # print('{:<{}s}'.format(str(line[value[0]]), value[1]), end='')
        # print()
        lineitems.append(createtime)
        sqlclause = "insert into tx3result  (equip_type, equip_level, price, equ_xiuwei, lian_hu, jiahu, mattack_max, mattack_min, pattack_max, pattack_min, castspeed, movespeed, pdef, avoid, mdef, hit, huixin, wan_jun, yu_xin, zhu_xin, equip_name, createtime) values(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sqlclause, args=tuple(lineitems))
        print(tuple(lineitems))

        if len(result['msg']) != 15:
            conn.commit()
            cur.close()
            conn.close()
            exit(3)
    conn.commit()
    time.sleep(random.randrange(1, 5))
    pgnum += 1
