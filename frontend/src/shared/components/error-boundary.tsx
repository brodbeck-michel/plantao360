/**
 * ErrorBoundary — Plantão 360
 *
 * Error boundary para capturar erros de renderização.
 * Reutilizável por todas as features.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { ErrorOutline } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onReset?: () => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

// ============================================================
// Component
// ============================================================

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    this.props.onReset?.();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          py={8}
          px={4}
        >
          <ErrorOutline sx={{ fontSize: 64, color: 'error.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            Algo deu errado
          </Typography>
          <Typography variant="body2" color="text.secondary" textAlign="center" mb={3}>
            Ocorreu um erro inesperado. Tente novamente ou entre em contato com o suporte.
          </Typography>
          <Button variant="contained" onClick={this.handleReset}>
            Tentar Novamente
          </Button>
        </Box>
      );
    }

    return this.props.children;
  }
}
