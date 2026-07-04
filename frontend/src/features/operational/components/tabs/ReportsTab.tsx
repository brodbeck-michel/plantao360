import React, { useMemo } from 'react';
import { Box, Typography, Paper, Button, List, ListItem, ListItemIcon, ListItemText, Alert } from '@mui/material';
import {
  Description as PdfIcon,
  TableChart as ExcelIcon,
  Code as CsvIcon,
  Assessment as ReportIcon,
} from '@mui/icons-material';
import { SHIFT_TYPES, SHIFT_LABELS, SHIFT_TIMES, MONTH_NAMES } from '../../types/operational-types';
import type { WorkspaceSummary, DayData, DoctorOption, PeriodInfo } from '../../types/operational-types';

interface ReportsTabProps {
  period: PeriodInfo;
  summary: WorkspaceSummary;
  days: DayData[];
  doctors: DoctorOption[];
}

function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export function ReportsTab({ period, summary, days, doctors }: ReportsTabProps) {
  const monthName = MONTH_NAMES[period.month - 1];

  const generateCSV = () => {
    let csv = 'Data,Dia,Tipo Turno,Horario,Medico,CRM,Especialidade,Status\n';
    days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        const cell = day.shifts[st];
        cell.assignments.forEach((a) => {
          const doc = doctors.find((d) => d.id === a.doctor_id);
          csv += `${day.date},${day.day_of_week},"${SHIFT_LABELS[st]}",${a.start_time}-${a.end_time},"${a.doctor_name}","${doc?.crm || ''}","${doc?.specialty || ''}",${a.status}\n`;
        });
      });
    });
    downloadFile(csv, `escala_${period.year}_${String(period.month).padStart(2, '0')}.csv`, 'text/csv;charset=utf-8');
  };

  const generateExcel = () => {
    let xml = '<?xml version="1.0"?>\n<?mso-application progid="Excel.Sheet"?>\n<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet">\n<Worksheet ss:Name="Escala">\n<Table>\n';
    xml += `<Row><Cell><Data ss:Type="String">Escala ${monthName} ${period.year}</Data></Cell></Row>\n`;
    xml += `<Row><Cell><Data ss:Type="String">Cobertura: ${summary.coverage_rate}%</Data></Cell><Cell><Data ss:Type="String">Turnos: ${summary.filled_shifts}/${summary.total_shifts}</Data></Cell><Cell><Data ss:Type="String">Horas: ${summary.total_hours}h</Data></Cell></Row>\n`;
    xml += '<Row></Row>\n';
    xml += '<Row>';
    ['Data', 'Dia', 'Tipo', 'Horario', 'Medico', 'CRM', 'Especialidade', 'Status'].forEach((h) => {
      xml += `<Cell><Data ss:Type="String">${h}</Data></Cell>`;
    });
    xml += '</Row>\n';
    days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          const doc = doctors.find((d) => d.id === a.doctor_id);
          xml += '<Row>';
          [day.date, day.day_of_week, SHIFT_LABELS[st], `${a.start_time}-${a.end_time}`, a.doctor_name, doc?.crm || '', doc?.specialty || '', a.status].forEach((v) => {
            xml += `<Cell><Data ss:Type="String">${v}</Data></Cell>`;
          });
          xml += '</Row>\n';
        });
      });
    });
    xml += '</Table>\n</Worksheet>\n</Workbook>';
    downloadFile(xml, `escala_${period.year}_${String(period.month).padStart(2, '0')}.xls`, 'application/vnd.ms-excel');
  };

  const generatePDF = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    let html = `<!DOCTYPE html><html><head><title>Escala ${monthName} ${period.year}</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      h1 { color: #00995D; font-size: 20px; }
      h2 { font-size: 14px; color: #374151; margin-top: 20px; }
      table { width: 100%; border-collapse: collapse; margin-top: 10px; }
      th, td { border: 1px solid #E5E7EB; padding: 6px 8px; font-size: 11px; text-align: left; }
      th { background: #F3F4F6; font-weight: 600; }
      .summary { display: flex; gap: 20px; margin: 10px 0; }
      .summary span { font-size: 12px; }
      @media print { body { padding: 10px; } }
    </style></head><body>
    <h1>Escala ${monthName} ${period.year}</h1>
    <p style="color:#6B7280;font-size:12px">PS Unimed Tubarao - Periodo: 26/${String(period.month).padStart(2, '0')}/${period.year} a 25/${String(period.month === 12 ? 1 : period.month + 1).padStart(2, '0')}/${period.month === 12 ? period.year + 1 : period.year}</p>
    <div class="summary">
      <span><strong>Cobertura:</strong> ${summary.coverage_rate}%</span>
      <span><strong>Turnos:</strong> ${summary.filled_shifts}/${summary.total_shifts}</span>
      <span><strong>Horas:</strong> ${summary.total_hours}h</span>
      <span><strong>Medicos:</strong> ${summary.total_doctors}</span>
    </div>
    <table><thead><tr><th>Data</th><th>Dia</th><th>Turno</th><th>Horario</th><th>Medico</th><th>CRM</th><th>Especialidade</th></tr></thead><tbody>`;
    days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          const doc = doctors.find((d) => d.id === a.doctor_id);
          html += `<tr><td>${day.date}</td><td>${day.day_of_week}</td><td>${SHIFT_LABELS[st]}</td><td>${a.start_time}-${a.end_time}</td><td>${a.doctor_name}</td><td>${doc?.crm || ''}</td><td>${doc?.specialty || ''}</td></tr>`;
        });
      });
    });
    html += '</tbody></table>';
    html += `<h2>Financeiro</h2><table><thead><tr><th>Medico</th><th>CRM</th><th>Plantoes</th><th>Horas</th><th>Vlr/Hora</th><th>Total</th></tr></thead><tbody>`;
    const financials = doctors.map((d) => {
      let totalHours = 0;
      let shiftCount = 0;
      days.forEach((day) => {
        SHIFT_TYPES.forEach((st) => {
          day.shifts[st].assignments.forEach((a) => {
            if (a.doctor_id === d.id) {
              shiftCount++;
              const parts_s = a.start_time.split(':');
              const parts_e = a.end_time.split(':');
              let startMin = parseInt(parts_s[0]) * 60 + parseInt(parts_s[1]);
              let endMin = parseInt(parts_e[0]) * 60 + parseInt(parts_e[1]);
              if (endMin <= startMin) endMin += 24 * 60;
              totalHours += (endMin - startMin) / 60;
            }
          });
        });
      });
      return { ...d, totalHours, shiftCount, totalValue: totalHours * d.hour_rate };
    }).filter((d) => d.shiftCount > 0).sort((a, b) => b.totalValue - a.totalValue);
    financials.forEach((d) => {
      html += `<tr><td>${d.name}</td><td>${d.crm}</td><td>${d.shiftCount}</td><td>${d.totalHours.toFixed(1)}h</td><td>R$ ${d.hour_rate.toFixed(2)}</td><td>R$ ${d.totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td></tr>`;
    });
    html += '</tbody></table>';
    html += '<script>window.onload=function(){window.print();}</script></body></html>';
    printWindow.document.write(html);
    printWindow.document.close();
  };

  const generateCoverageReport = () => {
    let csv = 'Data,Dia,T1,T2,T3,R1,R2,Total Preenchidos,Total Vagas,Cobertura %\n';
    days.forEach((day) => {
      const row: Record<string, string | number> = { date: day.date, dow: day.day_of_week };
      let filled = 0;
      SHIFT_TYPES.forEach((st) => {
        const count = day.shifts[st].assignments.length;
        row[st] = count;
        filled += count;
      });
      row.total_filled = filled;
      row.total_slots = SHIFT_TYPES.length;
      row.coverage = ((filled / SHIFT_TYPES.length) * 100).toFixed(1);
      csv += `${row.date},${row.dow},${row.T1},${row.T2},${row.T3},${row.R1},${row.R2},${row.total_filled},${row.total_slots},${row.coverage}%\n`;
    });
    downloadFile(csv, `cobertura_${period.year}_${String(period.month).padStart(2, '0')}.csv`, 'text/csv;charset=utf-8');
  };

  const reports = [
    { icon: <PdfIcon />, label: 'Escala PDF', desc: 'Relatorio completo para impressao', action: generatePDF },
    { icon: <ExcelIcon />, label: 'Escala Excel', desc: 'Planilha com todos os turnos e medicos', action: generateExcel },
    { icon: <CsvIcon />, label: 'Escala CSV', desc: 'Dados brutos para importacao', action: generateCSV },
    { icon: <ReportIcon />, label: 'Analise de Cobertura', desc: 'Cobertura diaria por tipo de turno', action: generateCoverageReport },
  ];

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Typography variant="h6" fontWeight={700} mb={3}>Relatorios</Typography>
      <Alert severity="info" sx={{ mb: 2 }}>Todos os relatorios sao gerados imediatamente a partir dos dados atuais da competencia.</Alert>
      <List>
        {reports.map((r, i) => (
          <ListItem key={i} sx={{ bgcolor: 'background.paper', mb: 1, borderRadius: 1, border: '1px solid #E5E7EB' }}>
            <ListItemIcon>{r.icon}</ListItemIcon>
            <ListItemText primary={r.label} secondary={r.desc} />
            <Button variant="outlined" size="small" onClick={r.action} sx={{ borderColor: '#00995D', color: '#00995D', '&:hover': { borderColor: '#007A4D', bgcolor: '#F0FDF4' } }}>Gerar</Button>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
