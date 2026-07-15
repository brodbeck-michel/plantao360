import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import MainLayout from './layouts/MainLayout';
import { ROUTES } from './routes/routes';
import { useAuth } from './contexts/AuthContext';
import LoginPage from './pages/LoginPage';

const HomePage = React.lazy(() => import('./pages/HomePage'));
const HealthPage = React.lazy(() => import('./pages/HealthPage'));
const DashboardPage = React.lazy(() => import('./features/dashboard/pages/dashboard-page'));
const DoctorListPage = React.lazy(() => import('./features/doctor/pages/doctor-list-page').then((m) => ({ default: m.DoctorListPage })));
const DoctorDetailPage = React.lazy(() => import('./features/doctor/pages/doctor-detail-page').then((m) => ({ default: m.DoctorDetailPage })));
const WorkspacePage = React.lazy(() => import('./features/operational/pages/workspace-page'));
const WorkspaceRedirect = React.lazy(() => import('./features/operational/pages/workspace-redirect').then((m) => ({ default: m.WorkspaceRedirect })));
const PeriodListPage = React.lazy(() => import('./features/period/pages/period-list-page').then((m) => ({ default: m.PeriodListPage })));
const ShiftListPage = React.lazy(() => import('./features/shift/pages/shift-list-page').then((m) => ({ default: m.ShiftListPage })));
const UserListPage = React.lazy(() => import('./pages/UserListPage'));
const AccessDeniedPage = React.lazy(() => import('./pages/AccessDeniedPage'));

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

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <PageLoader />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, hasRole } = useAuth();

  if (isLoading) {
    return <PageLoader />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!hasRole('ADMIN')) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return <>{children}</>;
}

function App() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <PageLoader />;
  }

  return (
    <Routes>
      <Route path={ROUTES.LOGIN} element={isAuthenticated ? <Navigate to={ROUTES.DASHBOARD} replace /> : <LoginPage />} />

      <Route element={<PrivateRoute><MainLayout /></PrivateRoute>}>
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

        <Route path={ROUTES.USERS} element={<AdminRoute><LazyPage><UserListPage /></LazyPage></AdminRoute>} />

        <Route path="/access-denied" element={<LazyPage><AccessDeniedPage /></LazyPage>} />
      </Route>
    </Routes>
  );
}

export default App;
