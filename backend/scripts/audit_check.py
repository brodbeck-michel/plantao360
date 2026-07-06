import sqlite3
conn = sqlite3.connect('/app/data/plantao360.db')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND status != 'cancelled'")
print('Non-cancelled:', c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND status = 'cancelled'")
print('Cancelled:', c.fetchone()[0])
conn.close()
