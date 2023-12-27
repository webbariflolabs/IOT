from configparser import ConfigParser 
import psycopg2 
from datetime import datetime

  
def connect(device_id): 
    """ Connect to the PostgreSQL database server """
    print("entering the connect func")
    conn = None
    device_id=device_id
    # Ph = "'Ph'"
    # ORP = "'ORP'"
    # DO = "'DO'"
    # Current = "'Current'"
    # voltage = "'voltage'"
    # CPU_TEMPERATURE = "'CPU_TEMPERATURE'"

    current_time = datetime.now()
    current_time_str = current_time.strftime("'%H:%M:%S'")
    current_date_str = current_time.strftime("'%Y-%m-%d'")

    try: 
        params = {
            'host':'20.244.48.88',
            'database':'iot',
            'user':'bariflolabs',
            'password':'bariflo123'
            } 

        print('Connecting to the PostgreSQL database...') 
        conn = psycopg2.connect(**params)  
        cur = conn.cursor() 
        cur.execute(f'select param_type,param_value from public.app1_parameter where "device_id"={device_id} order by id desc limit 120;')  
        data = cur.fetchall()
        print(data)
        Sensor1=[]
        Sensor2=[]
        Sensor3=[]
        Sensor4=[]

        

        for i in data[::-1]:
            a = [m for m in i]
            if a[0]=='Sensor1':
                Sensor1.append(a[1])
            if a[0]=='Sensor2':
                Sensor2.append(a[1])
            if a[0]=='Sensor3':
                Sensor3.append(a[1])
            if a[0]=='Sensor4':
                Sensor4.append(a[1])
            # if a[0]=='Current':
            #     Current.append(a[1])
            # if a[0]=='Ph':
            #     ph.append(a[1])
        # print(orp)

        cur.execute(f'SELECT time FROM public.app1_parameter where "device_id" = {device_id} ORDER BY id DESC LIMIT 60;')  
        # time = list(set([str((i[0])) for i in cur.fetchall()]))
        time =[str((i[0])) for i in cur.fetchall()]
        time.reverse()
        time_stamp=[]
        for i in time:
            if i not in time_stamp:
                time_stamp.append(i)

        # if not Sensor1 and Sensor2 and Sensor3 and Sensor4:
        #     import os
        #     
        return {
                'Sensor1':Sensor1,
                'Sensor2':Sensor2,
                'Sensor3':Sensor3,
                'Sensor4':Sensor4,
                'time':time_stamp
                }

        # cur.close() 
 
    except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 

    # finally: 
    #     if conn is not None: 
    #         conn.close() 
    #         print('Database connection closed.') 
  
  
if __name__ == '__main__': 
    connect()
