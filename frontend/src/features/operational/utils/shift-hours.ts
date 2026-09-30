/**
 * Horas de um turno da escala para fins de calculo (PLANTAOPA-5).
 *
 * Os turnos sao cadastrados "quebrados" (ex: 13:00-18:59), o que tirava 1 min
 * de cada plantao no Financeiro. Para o calculo vale a hora cheia:
 * 13:00-18:59 conta como 6h. Hora extra NAO passa por aqui — usa o valor lancado.
 */
export function shiftHours(startTime: string, endTime: string): number {
  const [sh, sm] = startTime.split(':').map((p) => parseInt(p, 10));
  const [eh, em] = endTime.split(':').map((p) => parseInt(p, 10));
  if ([sh, sm, eh, em].some(Number.isNaN)) return 0;
  const startMin = sh * 60 + sm;
  let endMin = eh * 60 + em;
  if (endMin <= startMin) endMin += 24 * 60;
  return Math.round((endMin - startMin) / 60);
}

export function compareDoctorName(a: { name: string }, b: { name: string }): number {
  return a.name.localeCompare(b.name, 'pt-BR', { sensitivity: 'base' });
}
