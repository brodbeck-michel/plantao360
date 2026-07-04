import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import MainLayout from './layouts/MainLayout';
import { ROUTES } from './routes/routes';

const HomePage = React.lazy(() => import('./pages/HomePage'));
const HealthPage = React.lazy(() => import('./pages/HealthPage'));
const DashboardPage = React.lazy(() => import('./features/dashboard/pages/dashboard-page'));
const DoctorListPage = React.lazy(() => import('./features/doctor/pages/doctor-list-page').then((m) => ({ default: m.DoctorListPage })));
const DoctorDetailPage = React.lazy(() => import('./features/doctor/pages/doctor-detail-page').then((m) => ({ default: m.DoctorDetailPage })));
const WorkspacePage = React.lazy(() => import('./features/operational/pages/workspace-page'));
const WorkspaceRedirect = React.lazy(() => import('./features/operational/pages/workspace-redirect').then((m) => ({ default: m.WorkspaceRedirect })));
const PeriodListPage = React.lazy(() => import('./features/period/pages/period-list-page').then((m) => ({ default: m.PeriodListPage })));
const ShiftListPage = React.lazy(() => import('./features/shift/pages/shift-list-page').then((m) => ({ default: m.ShiftListPage })));

function PageLoader() {
  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="40vh">
      <CircularProgress size={40} />
    </Box>
  );
}

function LazyPage({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<PageLoader />}>{children}</Suspense>;
}

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path={ROUTES.HOME} element={<LazyPage><HomePage /></LazyPage>} />
        <Route path={ROUTES.HEALTH} element={<LazyPage><HealthPage /></LazyPage>} />
        <Route path={ROUTES.DASHBOARD} element={<LazyPage><DashboardPage /></LazyPage>} />
        <Route path={ROUTES.WORKSPACE} element={<LazyPage><WorkspaceRedirect /></LazyPage>} />

        <Route path={ROUTES.DOCTORS} element={<LazyPage><DoctorListPage /></LazyPage>} />
        <Route path={ROUTES.DOCTOR_NEW} element={<LazyPage><DoctorListPage /></LazyPage>} />
        <Route path={ROUTES.DOCTOR_DETAIL} element={<LazyPage><DoctorDetailPage /></LazyPage>} />
        <Route path={ROUTES.DOCTOR_EDIT} element={<LazyPage><DoctorDetailPage /></LazyPage>} />

        <Route path={ROUTES.PERIODS} element={<LazyPage><PeriodListPage /></LazyPage>} />
        <Route path={ROUTES.PERIOD_NEW} element={<LazyPage><PeriodListPage /></LazyPage>} />
        <Route path={ROUTES.PERIOD_DETAIL} element={<LazyPage><WorkspacePage /></LazyPage>} />
        <Route path={ROUTES.PERIOD_EDIT} element={<LazyPage><WorkspacePage /></LazyPage>} />

        <Route path={ROUTES.SHIFTS} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.SHIFT_NEW} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.SHIFT_DETAIL} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.SHIFT_EDIT} element={<LazyPage><ShiftListPage /></LazyPage>} />

        <Route path={ROUTES.ASSIGNMENTS} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.ASSIGNMENT_NEW} element={<LazyPage><ShiftListPage /></LazyPage>} />

        <Route path={ROUTES.COVERAGE} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.EXTRAS} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.PAYROLL} element={<LazyPage><ShiftListPage /></LazyPage>} />
        <Route path={ROUTES.ANALYTICS} element={<LazyPage><DashboardPage /></LazyPage>} />
        <Route path={ROUTES.TIMELINE} element={<LazyPage><DashboardPage /></LazyPage>} />
        <Route path={ROUTES.REPORTS} element={<LazyPage><DashboardPage /></LazyPage>} />
        <Route path={ROUTES.READINESS} element={<LazyPage><DashboardPage /></LazyPage>} />
      </Route>
    </Routes>
  );
}

export default App;
