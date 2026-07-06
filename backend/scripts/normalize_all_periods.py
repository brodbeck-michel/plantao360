"""Normalize all legacy periods (1-5) to have all 5 shift types per day.

Each period covers 26th of month → 25th of next month.
For each day in the competency range, ensures T1, T2, T3, R1, R2 exist.
Does NOT touch existing assignments or doctors.
"""
import sqlite3
from datetime import date, timedelta

DB_PATH = '/app/data/plantao360.db'

ALL_TYPES = ['T1', 'T2', 'T3', 'R1', 'R2']

SHIFT_TIMES = {
    'T1': ('07:00:00', '19:00:00', 720),
    'T2': ('19:00:00', '07:00:00', 720),
    'T3': ('07:00:00', '07:00:00', 1440),
    'R1': ('09:00:00', '14:59:00', 360),
    'R2': ('15:00:00', '21:00:00', 360),
}


def get_competency_dates(year, month):
    """Return (start_date, end_date) for competency: 26th of month → 25th of next."""
    start = date(year, month, 26)
    if month == 12:
        end = date(year + 1, 1, 25)
    else:
        end = date(year, month + 1, 25)
    return start, end


def normalize_period(conn, period_id, year, month):
    start, end = get_competency_dates(year, month)
    c = conn.cursor()

    # Get existing shifts
    c.execute('SELECT shift_date, shift_type FROM shifts WHERE period_id=?', (period_id,))
    existing = set((r[0], r[1]) for r in c.fetchall())
    existing_count = len(existing)

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
                    (period_id, iso, st, 'draft', sched_start, sched_end, dur, 1)
                )
                added += 1
                existing.add((iso, st))
        current += timedelta(days=1)

    conn.commit()

    # Verify
    c.execute('SELECT shift_type, COUNT(*) FROM shifts WHERE period_id=? GROUP BY shift_type ORDER BY shift_type', (period_id,))
    types = dict(c.fetchall())
    total = sum(types.values())
    missing_types = [t for t in ALL_TYPES if t not in types or types[t] < 30]

    print('Period %d (%d/%d): %d existing → %d added → %d total' % (
        period_id, year, month, existing_count, added, total))
    print('  Types: %s' % types)
    if missing_types:
        print('  WARNING: missing/incomplete types: %s' % missing_types)
    else:
        print('  OK: all 5 types with 30 days each')

    return added


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get all periods
    c.execute('SELECT id, year, month, status FROM periods ORDER BY id')
    periods = c.fetchall()

    total_added = 0
    for pid, year, month, status in periods:
        added = normalize_period(conn, pid, year, month)
        total_added += added

    # Verify no orphaned assignments
    c.execute('''
        SELECT COUNT(*) FROM shift_parts sp
        WHERE NOT EXISTS (SELECT 1 FROM shifts s WHERE s.id = sp.shift_id)
    ''')
    orphans = c.fetchone()[0]

    print('')
    print('=' * 60)
    print('SUMMARY')
    print('Total shifts added across all periods: %d' % total_added)
    print('Orphaned assignments: %d' % orphans)

    # Final count per period
    c.execute('''
        SELECT p.id, p.year, p.month, COUNT(s.id) as total,
            SUM(CASE WHEN s.shift_type='T1' THEN 1 ELSE 0 END) as T1,
            SUM(CASE WHEN s.shift_type='T2' THEN 1 ELSE 0 END) as T2,
            SUM(CASE WHEN s.shift_type='T3' THEN 1 ELSE 0 END) as T3,
            SUM(CASE WHEN s.shift_type='R1' THEN 1 ELSE 0 END) as R1,
            SUM(CASE WHEN s.shift_type='R2' THEN 1 ELSE 0 END) as R2
        FROM periods p
        LEFT JOIN shifts s ON s.period_id = p.id
        GROUP BY p.id
        ORDER BY p.id
    ''')
    print('')
    print('Period  | Total |  T1 |  T2 |  T3 |  R1 |  R2')
    print('-' * 55)
    for r in c.fetchall():
        pid, y, m, total, t1, t2, t3, r1, r2 = r
        print('  %d/%d  |  %3d  | %3d | %3d | %3d | %3d | %3d' % (y, m, total or 0, t1 or 0, t2 or 0, t3 or 0, r1 or 0, r2 or 0))

    conn.close()


if __name__ == '__main__':
    main()
