import sqlite3
import random
from datetime import date, timedelta

random.seed(42)

conn = sqlite3.connect('/app/data/plantao360.db')
c = conn.cursor()

c.execute('DELETE FROM shift_parts')
print('Deleted shift_parts:', c.rowcount)
c.execute('DELETE FROM shifts')
print('Deleted shifts:', c.rowcount)
conn.commit()

c.execute('SELECT id, year, month FROM periods ORDER BY id')
periods = c.fetchall()

SHIFT_TYPES = ['T1', 'T2', 'T3']
SHIFT_TIMES = {
    'T1': ('07:00:00', '19:00:00', 720),
    'T2': ('19:00:00', '07:00:00', 720),
    'T3': ('07:00:00', '07:00:00', 1440),
}

c.execute('SELECT id FROM doctors WHERE active=1')
doctor_ids = [r[0] for r in c.fetchall()]
if not doctor_ids:
    c.execute('SELECT id FROM doctors')
    doctor_ids = [r[0] for r in c.fetchall()]

total_shifts = 0

for pid, year, month in periods:
    if month == 12:
        start = date(year, month, 26)
        end = date(year + 1, 1, 25)
    else:
        start = date(year, month, 26)
        end = date(year, month + 1, 25)

    current = start
    shift_count = 0
    used_keys = set()
    while current <= end:
        num_shifts = random.randint(1, 2)
        avail = list(SHIFT_TYPES)
        random.shuffle(avail)
        chosen = avail[:num_shifts]
        for st in chosen:
            key = (pid, current.isoformat(), st)
            if key in used_keys:
                continue
            used_keys.add(key)
            st_start, st_end, dur = SHIFT_TIMES[st]
            sched_start = current.isoformat() + 'T' + st_start
            if st_end <= st_start:
                sched_end = (current + timedelta(days=1)).isoformat() + 'T' + st_end
            else:
                sched_end = current.isoformat() + 'T' + st_end

            c.execute(
                'INSERT INTO shifts (period_id, shift_date, shift_type, status, scheduled_start, scheduled_end, actual_start, actual_end, total_duration_minutes, doctor_count, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
                (pid, current.isoformat(), st, 'draft', sched_start, sched_end, dur),
            )
            shift_id = c.lastrowid
            doctor_id = random.choice(doctor_ids)
            c.execute(
                'INSERT INTO shift_parts (shift_id, doctor_id, start_time, end_time, status, duration_minutes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
                (shift_id, doctor_id, st_start, st_end, 'planned', dur),
            )
            shift_count += 1
        current += timedelta(days=1)

    print(f'Period {pid} ({year}/{month:02d}): {shift_count} shifts ({start} to {end})')
    total_shifts += shift_count

conn.commit()
print(f'Total: {total_shifts} shifts created')

for pid, year, month in periods:
    c.execute('SELECT MIN(shift_date), MAX(shift_date), COUNT(*) FROM shifts WHERE period_id=?', (pid,))
    r = c.fetchone()
    print(f'Period {pid}: {r[0]} to {r[1]}, count={r[2]}')

conn.close()
