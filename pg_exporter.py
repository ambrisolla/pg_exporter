import psycopg2
import configparser
import os
import subprocess as sb
import datetime

"""
    
    This Class was created to get some PostgreSQL metrics
    and export to Prometheus format

    Author      :   André Müzel Brisolla
    E-mail      :   andremuzel@gmail.com
    Date/Time   :   Nov 21 2021, 18:24
    Version     :   0.1

"""

class Exporter:

    def __init__(self):
        # Set script path directory
        self.fullpath = os.path.abspath(os.path.dirname(__file__))
        
        # Load configs
        config = configparser.ConfigParser()
        config.read('{}/config.ini'.format(self.fullpath))

        # Set hostname
        ps = sb.Popen('hostname', shell=True, stderr=sb.PIPE, stdout=sb.PIPE)
        ps.wait()
        self.hostname = ps.communicate()[0].decode('utf-8').replace('\n','')

        # Create connection
        self.conn = psycopg2.connect(
            host=config['PSQL']['PSQL_HOST'], 
            user=config['PSQL']['PSQL_USER'], 
            password=config['PSQL']['PSQL_PASS'])
    
    """
        Execute query
    """
    def query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        # Parse fields/columns
        columns = [ x[0] for x in cursor.description ]
        # Parse data
        result = []
        for row in data:
            row_list = {}
            for i,c in enumerate(row):
                if isinstance(row[i], datetime.datetime):
                    row_value = str(row[i])
                else:
                    row_value = row[i]
                row_list[columns[i]] = row_value
            result.append(row_list)
        return result

    """
        Generate Prometheus metrics
    """
    def generate_metrics(self, **kwargs):
        data = kwargs['data']
        basename = kwargs['basename']
        str_output = ''
        for row in data:
            labels = []
            numbers = []
            for item in row:
                value = row[item]
                is_number = isinstance(value, int) or isinstance(value, float)
                not_bool = not isinstance(value,bool)
                if is_number and not_bool: 
                    numbers.append({
                        'name' : item,
                        'value' : value
                    })
                else:
                    labels.append({
                        'name' : item,
                        'value' : value
                    })
            
            # Set label
            label = ','.join([ f"{x['name']}=\"{x['value']}\"" for x in labels ])

            # Create metrics
            for n in numbers:
                metric_name = n['name']
                metric_value = n['value']
                str = '{}_{}{{{}}} {}\n'.format(basename,metric_name,label,metric_value)
                str_output = str_output + str
        return str_output
            

    """
        Monitor stats: https://www.postgresql.org/docs/9.6/monitoring-stats.html
    """
    def get_monitor_stats(self):
        tables = ['pg_locks','pg_stat_activity','pg_stat_replication','pg_stat_database','pg_stat_database_conflicts']
        str_output = ''
        for table in tables:
            query = f'SELECT * from {table}'
            data = self.query(query)
            metrics = self.generate_metrics(data=data,basename="{}".format(table))
            if metrics != "":
                str_output = str_output + '{}'.format(metrics)
        return str_output

    """
        pg_settings
    """
    def pg_settings(self):
        query = 'table pg_settings'
        data = self.query(query)
        str_output = ""
        for item in data:
            name = item['name']
            setting = item['setting']
            # Try int
            try:
                int_value = int(setting)
                str_output = str_output + 'pg_settings_{} {}\n'.format(name,int_value)
            except:
                pass
            # On/Off data
            if setting == 'on' or setting == 'off':
                new_setting = setting.replace('on','1').replace('off','0')
                str_output = str_output + 'pg_settings_{} {}\n'.format(name,int(new_setting))
        return str_output
            
    """
        Get All Metrics
    """
    def metrics(self):
        all_metrics = self.get_monitor_stats() + self.pg_settings()
        return all_metrics

if __name__ == '__main__':
    e = Exporter()
    print(e.metrics())