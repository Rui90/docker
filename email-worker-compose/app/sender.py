import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.queue = redis.StrictRedis(host=redis_host, port=6379, db=0)

        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        dsn = f'dbname={db_name} user={db_user} host={db_host}'
        self.conn = psycopg2.connect(dsn)

    def register_message(self, subject, body):
        SQL = 'INSERT INTO emails (subject, body) VALUES (%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (subject, body))
        self.conn.commit()
        cur.close()
        msg = {'subject': subject, 'body': body}
        self.queue.rpush('sender', json.dumps(msg))
        print('Message saved')

    def send(self):
        subject = request.forms.get('subject')
        body = request.forms.get('body')
        self.register_message(subject, body)
        return 'Message in queue ! Subject: {} Body: {}'.format(subject, body)

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
