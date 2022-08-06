import threading
import time
import mysql.connector

from datetime import datetime
from EncryptionProcessor import EncryptionProcessor

def check_mysql_conn():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='engine',
            passwd='jagalah1234',
            database='distributed_encryption'
        )
    except mysql.connector.Error as err:
        # print('Koneksi Gagal')
        return None
    else:
        # print('Koneksi Berhasil')
        return conn

def check_available_job():
    conn = check_mysql_conn()
    if conn is not None:
        cur = conn.cursor()
        sql = 'SELECT * FROM t_jobs WHERE type_of_jobs=0 OR type_of_jobs=3 ORDER BY id_jobs ASC'
        cur.execute(sql)
        res = cur.fetchone()
        if res is not None:
            return res
        else:
            return None

def check_for_key_name(param):
    conn = check_mysql_conn()
    if conn is not None:
        cur = conn.cursor()
        sql = 'SELECT * FROM t_user_files WHERE id_user_files=\''+param+'\''
        cur.execute(sql)
        res = cur.fetchone()
        if res is not None:
            return res
        else:
            return None

def update_job_status(param):
    conn = check_mysql_conn()
    if conn is not None:
        cur = conn.cursor()
        sql = 'UPDATE t_jobs SET type_of_jobs=%s WHERE id_jobs=%s'
        val = param
        cur.execute(sql,val)
        conn.commit()
        res = cur.rowcount
        if res > 0:
            return True
        else:
            return None

def update_job_status2(param):
    conn = check_mysql_conn()
    if conn is not None:
        cur = conn.cursor()
        sql = 'UPDATE t_user_files SET status_user_files=%s WHERE id_user_files=%s'
        val = param
        cur.execute(sql,val)
        conn.commit()
        res = cur.rowcount
        if res > 0:
            return True
        else:
            return None

def update_date_start_job(param):
    conn = check_mysql_conn()
    if conn is not None:
        now = datetime.now()
        dateTime = now.strftime('%Y-%m-%d %H:%M:%S')
        cur = conn.cursor()
        sql = 'UPDATE t_jobs SET date_start_jobs=\''+dateTime+'\' WHERE id_jobs=\''+str(param)+'\''
        cur.execute(sql)
        conn.commit()
        res = cur.rowcount
        if res > 0:
            return True
        else:
            return None

def update_date_finish_job(param):
    conn = check_mysql_conn()
    if conn is not None:
        now = datetime.now()
        dateTime = now.strftime('%Y-%m-%d %H:%M:%S')
        cur = conn.cursor()
        sql = 'UPDATE t_jobs SET date_finish_jobs=\''+dateTime+'\' WHERE id_jobs=\''+str(param)+'\''
        cur.execute(sql)
        conn.commit()
        res = cur.rowcount
        if res > 0:
            return True
        else:
            return None

if __name__ == '__main__':
    print('---- System Starting ----')        
    while True:
        availJobs = check_available_job()
        if availJobs is not None:
            print(availJobs)
            keyName = check_for_key_name(availJobs[5])
            if keyName is not None:
                print(keyName)
                jobID = availJobs[0]
                fileName = availJobs[5]
                jobStatus = availJobs[4]
                keyName = keyName[6]
                encryptionProcessor = EncryptionProcessor()
                encryptionProcessor.set_fileName(fileName)
                encryptionProcessor.set_keyFileName(keyName)
                encryptionProcessor.set_workerIP(['10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5'])
                encryptionProcessor.get_AllWorkerRes()
                encryptionProcessor.do_SplitFile()
                encryptionProcessor.do_CalculateJobAllocation()
                if jobStatus is 0:
                    update_job_status(['1',jobID])
                    update_job_status2(['PENC',fileName])
                    update_date_start_job(jobID)
                    encryptionProcessor.do_Encrypt()
                    update_job_status(['2',jobID])
                    update_job_status2(['ENC',fileName])
                    update_date_finish_job(jobID)
                elif jobStatus is 3:
                    update_job_status(['4',jobID])
                    update_job_status2(['PDEC',fileName])
                    update_date_start_job(jobID)
                    encryptionProcessor.do_Decrypt()
                    encryptionProcessor.do_MergeFile()
                    update_job_status(['5',jobID])
                    update_job_status2(['DEC',fileName])
                    update_date_finish_job(jobID)
        else:
            print('antrian pekerjaan kosong.')
        time.sleep(1)
    print('---- System Ending ----')