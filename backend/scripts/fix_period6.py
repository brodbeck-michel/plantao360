import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect('/app/data/plantao360.db')
c = conn.cursor()

pid = 6
start = date(2026, 6, 26)
end = date(2026, 7, 25)
ALL_TYPES = ['T1', 'T2', 'T3', 'R1', 'R2']

SHIFT_TIMES = {
    'T1': ('07:00:00', '19:00:00', 720),
    'T2': ('19:00:00', '07:00:00', 720),
    'T3': ('07:00:00', '07:00:00', 1440),
    'R1': ('09:00:00', '14:59:00', 360),
    'R2': ('15:00:00', '21:00:00', 360),
}

# Get existing shifts
c.execute('SELECT shift_date, shift_type FROM shifts WHERE period_id=6')
existing = set((r[0], r[1]) for r in c.fetchall())
print('Existing: %d shifts' % len(existing))

# Add missing shifts with correct fields
added = 0
current = start
while current <= end:
    iso = current.isoformat()
    for st in ALL_TYPES:
        if (iso, st) not in existing:
            st_start, st_end, dur = SHIFT_TIMES[st]
            sched_start = iso + 'T' + st_start
            if st_end <= st_start:
                next_d = current + timedelta(days=1)
                sched_end = next_d.isoformat() + 'T' + st_end
            else:
                sched_end = iso + 'T' + st_end

            c.execute(
                'INSERT INTO shifts (period_id, shift_date, shift_type, status, scheduled_start, scheduled_end, total_duration_minutes, doctor_count, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
                (pid, iso, st, 'draft', sched_start, sched_end, dur, 1)
            )
            added += 1
    current += timedelta(days=1)

conn.commit()
print('Added: %d missing shifts' % added)

# Verify
c.execute('SELECT shift_type, COUNT(*) FROM shifts WHERE period_id=6 GROUP BY shift_type ORDER BY shift_type')
for r in c.fetchall():
    print('  %s: %d' % (r[0], r[1]))
c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=6')
print('Total: %d' % c.fetchone()[0])
c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=6 AND scheduled_start IS NOT NULL')
print('With scheduled_start: %d' % c.fetchone()[0])
c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=6 AND scheduled_end IS NOT NULL')
print('With scheduled_end: %d' % c.fetchone()[0])

# Create period 7 (August)
c.execute('SELECT COUNT(*) FROM periods WHERE year=2026 AND month=8')
if c.fetchone()[0] == 0:
    c.execute('INSERT INTO periods (year, month, status, created_at, updated_at) VALUES (2026, 8, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)', ('draft',))
    conn.commit()
    print('Created period 7 (Aug 2026)')

conn.close()
