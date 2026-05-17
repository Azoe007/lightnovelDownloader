import React, { createContext, useContext, useState, useCallback } from 'react';
import type { Novel, DownloadTask } from '../types';
import * as api from '../services/api';
import toast from 'react-hot-toast';

interface AppState {
  // Downloads
  downloads: DownloadTask[];
  isLoadingDownloads: boolean;
  
  // Library
  library: Novel[];
  isLoadingLibrary: boolean;
  hasMoreLibrary: boolean;
  
  // Favorites
  favorites: Novel[];
  isLoadingFavorites: boolean;
  
  // History
  history: Novel[];
  isLoadingHistory: boolean;
}

interface AppContextType extends AppState {
  // Downloads actions
  refreshDownloads: () => Promise<void>;
  startDownload: (url: string) => Promise<void>;
  pauseDownload: (id: number) => Promise<void>;
  resumeDownload: (id: number) => Promise<void>;
  cancelDownload: (id: number) => Promise<void>;
  
  // Library actions
  refreshLibrary: (search?: string) => Promise<void>;
  loadMoreLibrary: () => Promise<void>;
  
  // Favorites actions
  refreshFavorites: () => Promise<void>;
  toggleFavorite: (novel: Novel) => Promise<void>;
  isFavorite: (novelId: number) => boolean;
  
  // History actions
  refreshHistory: () => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const initialAppState: AppState = {
  downloads: [],
  isLoadingDownloads: false,
  library: [],
  isLoadingLibrary: false,
  hasMoreLibrary: true,
  favorites: [],
  isLoadingFavorites: false,
  history: [],
  isLoadingHistory: false,
};

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AppState>(initialAppState);
  const [librarySkip, setLibrarySkip] = useState(0);
  const libraryLimit = 20;

  // Downloads
  const refreshDownloads = useCallback(async () => {
    setState(s => ({ ...s, isLoadingDownloads: true }));
    try {
      const downloads = await api.getDownloads();
      setState(s => ({ ...s, downloads, isLoadingDownloads: false }));
    } catch (error) {
      setState(s => ({ ...s, isLoadingDownloads: false }));
      toast.error('Erreur lors du chargement des téléchargements');
    }
  }, []);

  const startDownload = useCallback(async (url: string) => {
    try {
      await api.startDownload(url);
      toast.success('Téléchargement démarré !');
      refreshDownloads();
    } catch (error) {
      toast.error("Erreur lors du démarrage du téléchargement");
    }
  }, [refreshDownloads]);

  const pauseDownload = useCallback(async (id: number) => {
    try {
      await api.pauseDownload(id);
      toast.success('Téléchargement mis en pause');
      refreshDownloads();
    } catch (error) {
      toast.error('Erreur lors de la mise en pause');
    }
  }, [refreshDownloads]);

  const resumeDownload = useCallback(async (id: number) => {
    try {
      await api.resumeDownload(id);
      toast.success('Téléchargement repris');
      refreshDownloads();
    } catch (error) {
      toast.error('Erreur lors de la reprise');
    }
  }, [refreshDownloads]);

  const cancelDownload = useCallback(async (id: number) => {
    try {
      await api.cancelDownload(id);
      toast.success('Téléchargement annulé');
      refreshDownloads();
    } catch (error) {
      toast.error('Erreur lors de l\'annulation');
    }
  }, [refreshDownloads]);

  // Library
  const refreshLibrary = useCallback(async (search?: string) => {
    setState(s => ({ ...s, isLoadingLibrary: true, library: [], hasMoreLibrary: true }));
    setLibrarySkip(0);
    try {
      const novels = await api.getLibrary({ skip: 0, limit: libraryLimit, search });
      setState(s => ({ 
        ...s, 
        library: novels, 
        isLoadingLibrary: false,
        hasMoreLibrary: novels.length >= libraryLimit
      }));
    } catch (error) {
      setState(s => ({ ...s, isLoadingLibrary: false }));
      toast.error('Erreur lors du chargement de la bibliothèque');
    }
  }, []);

  const loadMoreLibrary = useCallback(async () => {
    if (state.isLoadingLibrary || !state.hasMoreLibrary) return;
    
    const newSkip = librarySkip + libraryLimit;
    setState(s => ({ ...s, isLoadingLibrary: true }));
    setLibrarySkip(newSkip);
    
    try {
      const novels = await api.getLibrary({ skip: newSkip, limit: libraryLimit });
      setState(s => ({ 
        ...s, 
        library: [...s.library, ...novels],
        isLoadingLibrary: false,
        hasMoreLibrary: novels.length >= libraryLimit
      }));
    } catch (error) {
      setState(s => ({ ...s, isLoadingLibrary: false }));
      toast.error('Erreur lors du chargement de plus de novels');
    }
  }, [state.isLoadingLibrary, state.hasMoreLibrary, librarySkip]);

  // Favorites
  const refreshFavorites = useCallback(async () => {
    setState(s => ({ ...s, isLoadingFavorites: true }));
    try {
      const favorites = await api.getFavorites();
      setState(s => ({ ...s, favorites, isLoadingFavorites: false }));
    } catch (error) {
      setState(s => ({ ...s, isLoadingFavorites: false }));
      toast.error('Erreur lors du chargement des favoris');
    }
  }, []);

  const toggleFavorite = useCallback(async (novel: Novel) => {
    const isFav = state.favorites.some(f => f.id === novel.id);
    try {
      if (isFav) {
        await api.removeFavorite(novel.id);
        setState(s => ({ 
          ...s, 
          favorites: s.favorites.filter(f => f.id !== novel.id) 
        }));
        toast.success('Retiré des favoris');
      } else {
        await api.addFavorite(novel.id);
        setState(s => ({ 
          ...s, 
          favorites: [...s.favorites, novel] 
        }));
        toast.success('Ajouté aux favoris');
      }
    } catch (error) {
      toast.error('Erreur lors de la modification des favoris');
    }
  }, [state.favorites]);

  const isFavorite = useCallback((novelId: number) => {
    return state.favorites.some(f => f.id === novelId);
  }, [state.favorites]);

  // History
  const refreshHistory = useCallback(async () => {
    setState(s => ({ ...s, isLoadingHistory: true }));
    try {
      const history = await api.getHistory({ limit: 50 });
      setState(s => ({ ...s, history, isLoadingHistory: false }));
    } catch (error) {
      setState(s => ({ ...s, isLoadingHistory: false }));
      toast.error('Erreur lors du chargement de l\'historique');
    }
  }, []);

  const value: AppContextType = {
    ...state,
    refreshDownloads,
    startDownload,
    pauseDownload,
    resumeDownload,
    cancelDownload,
    refreshLibrary,
    loadMoreLibrary,
    refreshFavorites,
    toggleFavorite,
    isFavorite,
    refreshHistory,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};