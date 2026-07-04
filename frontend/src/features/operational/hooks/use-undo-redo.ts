import { useCallback, useRef, useState } from 'react';

export interface HistoryAction {
  id: string;
  label: string;
  undo: () => Promise<void>;
  redo: () => Promise<void>;
}

interface UseUndoRedoProps {
  maxHistory?: number;
  onStatusChange?: (status: 'saved' | 'saving' | 'error') => void;
}

export function useUndoRedo({ maxHistory = 50, onStatusChange }: UseUndoRedoProps = {}) {
  const [history, setHistory] = useState<HistoryAction[]>([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const idCounter = useRef(0);

  const push = useCallback(async (label: string, undoFn: () => Promise<void>, redoFn: () => Promise<void>) => {
    const action: HistoryAction = {
      id: `action-${++idCounter.current}`,
      label,
      undo: undoFn,
      redo: redoFn,
    };
    setHistory((prev) => {
      const newHistory = prev.slice(0, currentIndex + 1);
      newHistory.push(action);
      if (newHistory.length > maxHistory) newHistory.shift();
      return newHistory;
    });
    setCurrentIndex((prev) => Math.min(prev + 1, maxHistory - 1));
    onStatusChange?.('saved');
  }, [currentIndex, maxHistory, onStatusChange]);

  const undo = useCallback(async () => {
    if (currentIndex < 0 || currentIndex >= history.length) return;
    onStatusChange?.('saving');
    try {
      await history[currentIndex].undo();
      setCurrentIndex((prev) => prev - 1);
      onStatusChange?.('saved');
    } catch {
      onStatusChange?.('error');
    }
  }, [currentIndex, history, onStatusChange]);

  const redo = useCallback(async () => {
    if (currentIndex >= history.length - 1) return;
    onStatusChange?.('saving');
    try {
      await history[currentIndex + 1].redo();
      setCurrentIndex((prev) => prev + 1);
      onStatusChange?.('saved');
    } catch {
      onStatusChange?.('error');
    }
  }, [currentIndex, history, onStatusChange]);

  const clear = useCallback(() => {
    setHistory([]);
    setCurrentIndex(-1);
  }, []);

  const canUndo = currentIndex >= 0;
  const canRedo = currentIndex < history.length - 1;
  const pastActions = history.slice(0, currentIndex + 1).reverse();
  const futureActions = history.slice(currentIndex + 1);

  return {
    history,
    push,
    undo,
    redo,
    clear,
    canUndo,
    canRedo,
    pastActions,
    futureActions,
    undoCount: currentIndex + 1,
    redoCount: history.length - currentIndex - 1,
  };
}
