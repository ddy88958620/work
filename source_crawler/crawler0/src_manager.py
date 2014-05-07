
import MySQLdb


dbconf = {'host': '10.4.6.139', 'port': 3306, 'user': 'liuxi', 'pswd': 'moretvSlave@608', 'db': 'test', 'charset': 'utf8', 'table': 'channel'}
# dbconf = {'host': '10.4.6.139', 'port': 3306, 'user': 'liuxi', 'pswd': 'moretvSlave@608', 'db': 'moretv', 'charset': 'utf8', 'table': 'mtv_source'}


class Manager(object):
    def __init__(self):
        self.dbconf = dbconf

    def update(self, site, src_list):
        if site == 'cntv':
            self._update_cntv(src_list)
        elif site == 'cntv_fix':
            self._update_cntv_fix(src_list)
        elif site == 'qq':
            pass
        else:
            pass

    def _update_cntv(self, src_list):
        conn = MySQLdb.connect(host=dbconf['host'], user=dbconf['user'], passwd=dbconf['pswd'], port=dbconf['port'], db=dbconf['db'], charset=dbconf['charset'])
        cursor = conn.cursor()

        for src in src_list:
            # sql = "select * from %s where `code`='%s' and site='cntv'" % (dbconf['table'], src['code'])
            # count = cursor.execute(sql)
            # rows = cursor.fetchall()

            # if len(rows) > 0:
            #     sql = "update %s set url='%s' where `code`='%s' and site='cntv'" % (dbconf['table'], src['auth'], src['code'])
            # else:
            #     sql = "insert into %s (code, site, url, seq, status) values ('%s', '%s', '%s', 1, 1)" % (dbconf['table'], src['code'], 'cntv', src['auth'])

            sql = "replace into %s (code, site, url, seq, status) values ('%s', 'cntv', '%s', 1, 1)" % (dbconf['table'], src['code'], src['auth'])
            count = cursor.execute(sql)

        print "all cntv srcs saved"

    def _update_cntv_fix(self, src_list):
        conn = MySQLdb.connect(host=dbconf['host'], user=dbconf['user'], passwd=dbconf['pswd'], port=dbconf['port'], db=dbconf['db'], charset=dbconf['charset'])
        cursor = conn.cursor()

        for src in src_list:
            # sql = "select * from %s where `code`='%s' and site='cntv'" % (dbconf['table'], src['code'])
            # count = cursor.execute(sql)
            # rows = cursor.fetchall()

            # if len(rows) > 0:
            #     sql = "update %s set url='%s' where `code`='%s' and site='cntv'" % (dbconf['table'], src['auth'], src['code'])
            # else:
            #     sql = "insert into %s (code, site, url, seq, status) values ('%s', '%s', '%s', 1, 1)" % (dbconf['table'], src['code'], 'cntv', src['auth'])

            sql = "replace into %s (code, site, url, seq, status) values ('%s', 'cntv_hls', '%s', 1, 1)" % (dbconf['table'], src['code'], src['hls'])
            count = cursor.execute(sql)

            sql = "replace into %s (code, site, url, seq, status) values ('%s', 'cntv_flv', '%s', 1, 1)" % (dbconf['table'], src['code'], src['flv'])
            count = cursor.execute(sql)

        print "all cntv srcs saved"