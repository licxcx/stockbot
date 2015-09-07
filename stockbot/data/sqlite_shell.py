# -*- coding: utf-8 -*-
import sqlite3

def start_sqlite_shell():
    con = sqlite3.connect('stock.db')
    cur = con.cursor()
    buffer = ''
    print 'Enter your SQL commands to execute in sqlite3'
    print 'Enter a blank line to exit'
    while 1:
        line = raw_input()
        if line == '':
            break
        buffer += line
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()
                cur.execute(buffer)
                if buffer.lstrip().upper().startswith('SELECT'):
                    for record in cur.fetchall():
                        print record
            except sqlite3.Error, e:
                print 'An error occurred:', e.args[0]
            buffer = ''
    con.close()

if __name__ == '__main__':
    start_sqlite_shell()