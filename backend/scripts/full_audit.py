import sqlite3
import urllib.request
import json

conn = sqlite3.connect('/app/data/plantao360.db')
c = conn.cursor()

print('=' * 60)
print('AUDITORIA COMPLETA - COMPETENCIA JUNHO/2026 (Period 6)')
print('=' * 60)

# 1. Total de turnos e tipos
c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=6')
total = c.fetchone()[0]
c.execute('SELECT shift_type, COUNT(*) FROM shifts WHERE period_id=6 GROUP BY shift_type ORDER BY shift_type')
types = {r[0]: r[1] for r in c.fetchall()}
print('\n1. TOTAL DE TURNOS: %d (esperado: 150)' % total)
print('   Por tipo:', types)
all_5 = all(v == 30 for v in types.values())
print('   Todos com 30 registros: %s' % ('SIM' if all_5 else 'NAO'))

# 2. Cada dia com 5 tipos
c.execute('SELECT shift_date, shift_type FROM shifts WHERE period_id=6 ORDER BY shift_date, shift_type')
by_date = {}
for d, t in c.fetchall():
    by_date.setdefault(d, []).append(t)
expected = sorted(['T1', 'T2', 'T3', 'R1', 'R2'])
bad_days = [(d, sorted(ts)) for d, ts in by_date.items() if sorted(ts) != expected]
print('\n2. DIAS COM 5 TIPOS: %d/30 dias corretos' % (30 - len(bad_days)))
if bad_days:
    for d, ts in bad_days:
        print('   FALHA: %s tem %s' % (d, ts))
else:
    print('   Todos os 30 dias tem exatamente T1,T2,T3,R1,R2')

# 3. Dates dentro da competencia
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND shift_date < '2026-06-26'")
before = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND shift_date > '2026-07-25'")
after = c.fetchone()[0]
print('\n3. DATAS DENTRO DA COMPETENCIA (26/06 a 25/07):')
print('   Antes de 26/06: %d (esperado: 0)' % before)
print('   Depois de 25/07: %d (esperado: 0)' % after)
print('   Resultado: %s' % ('OK' if before == 0 and after == 0 else 'FALHA'))

# 4. Campos obrigatorios
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND scheduled_start IS NOT NULL")
has_start = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND scheduled_end IS NOT NULL")
has_end = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND total_duration_minutes IS NOT NULL")
has_dur = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM shifts WHERE period_id=6 AND doctor_count IS NOT NULL")
has_dc = c.fetchone()[0]
print('\n4. CAMPOS OBRIGATORIOS:')
print('   scheduled_start: %d/%d' % (has_start, total))
print('   scheduled_end: %d/%d' % (has_end, total))
print('   total_duration_minutes: %d/%d' % (has_dur, total))
print('   doctor_count: %d/%d' % (has_dc, total))
all_fields = has_start == total and has_end == total and has_dur == total and has_dc == total
print('   Resultado: %s' % ('OK' if all_fields else 'FALHA'))

# 5. Status validos
c.execute("SELECT DISTINCT status FROM shifts WHERE period_id=6")
statuses = [r[0] for r in c.fetchall()]
valid = {'draft', 'scheduled', 'in_progress', 'completed', 'cancelled'}
bad = [s for s in statuses if s not in valid]
print('\n5. STATUS VALIDOS:')
print('   Statuses encontrados:', statuses)
print('   Invalidos:', bad if bad else 'nenhum')
print('   Resultado: %s' % ('OK' if not bad else 'FALHA'))

# 6. Horarios por tipo
for st in ['T1', 'T2', 'T3', 'R1', 'R2']:
    c.execute("SELECT scheduled_start, scheduled_end, total_duration_minutes FROM shifts WHERE period_id=6 AND shift_type=? AND scheduled_start IS NOT NULL LIMIT 1", (st,))
    r = c.fetchone()
    if r:
        print('   %s: start=%s end=%s dur=%s' % (st, r[0], r[1], r[2]))

# 7. Shift_ids do workspace vs DB
print('\n6. WORKSPACE vs DB:')
r = urllib.request.urlopen('http://localhost:8000/api/v1/periods/6/workspace')
data = json.loads(r.read())['data']
ws_ids = set()
for day in data['days']:
    for t in ['T1', 'T2', 'T3', 'R1', 'R2']:
        sid = day['shifts'][t]['shift_id']
        if sid is not None:
            ws_ids.add(sid)
c.execute('SELECT id FROM shifts WHERE period_id=6')
db_ids = set(r[0] for r in c.fetchall())
missing = ws_ids - db_ids
print('   Workspace shift_ids: %d' % len(ws_ids))
print('   DB shift_ids: %d' % len(db_ids))
print('   In workspace but NOT in DB: %d %s' % (len(missing), missing if missing else ''))
print('   Resultado: %s' % ('OK' if not missing else 'FALHA'))

# 8. Assignments orfaos
c.execute('SELECT sp.id, sp.shift_id FROM shift_parts sp LEFT JOIN shifts s ON sp.shift_id=s.id WHERE s.id IS NULL')
orphans = c.fetchall()
print('\n7. ASSIGNMENTS ORFAOS: %d (esperado: 0)' % len(orphans))
if orphans:
    for o in orphans:
        print('   part_id=%s shift_id=%s' % o)
print('   Resultado: %s' % ('OK' if not orphans else 'FALHA'))

# 9. Comparacao com competencia nova (Julho)
c.execute('SELECT COUNT(*) FROM periods WHERE year=2026 AND month=7')
jul_exists = c.fetchone()[0]
if jul_exists:
    c.execute("SELECT id FROM periods WHERE year=2026 AND month=7")
    jul_pid = c.fetchone()[0]
    c.execute('SELECT shift_type, COUNT(*) FROM shifts WHERE period_id=? GROUP BY shift_type ORDER BY shift_type', (jul_pid,))
    jul_types = {r[0]: r[1] for r in c.fetchall()}
    c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=?', (jul_pid,))
    jul_total = c.fetchone()[0]
    print('\n8. COMPARACAO COM JULHO (period %d):' % jul_pid)
    print('   Julho shifts: %d' % jul_total)
    print('   Julho types:', jul_types)
else:
    print('\n8. Periodo Julho nao existe')

# 10. Periodos 1-5
print('\n9. PERIODOS 1-5 (LEGADOS):')
for pid in range(1, 6):
    c.execute('SELECT shift_type, COUNT(*) FROM shifts WHERE period_id=? GROUP BY shift_type ORDER BY shift_type', (pid,))
    types_p = {r[0]: r[1] for r in c.fetchall()}
    c.execute('SELECT COUNT(*) FROM shifts WHERE period_id=?', (pid,))
    total_p = c.fetchone()[0]
    has_r = 'R1' in types_p or 'R2' in types_p
    print('   Period %d: %d shifts, types=%s, has R1/R2=%s' % (pid, total_p, types_p, has_r))

print('\n' + '=' * 60)
print('FIM DA AUDITORIA')
print('=' * 60)

conn.close()
