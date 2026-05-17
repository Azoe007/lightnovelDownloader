import React, { useState, useEffect, useCallback } from 'react';
import { Search, X, BookOpen, ChevronDown } from 'lucide-react';
import { useApp } from '../context/AppContext';
import NovelCard from '../components/novel/NovelCard';

const LibraryPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const { 
    library, 
    isLoadingLibrary, 
    hasMoreLibrary, 
    refreshLibrary, 
    loadMoreLibrary 
  } = useApp();

  const handleSearch = useCallback(async (query: string) => {
    await refreshLibrary(query);
  }, [refreshLibrary]);

  const handleClearSearch = useCallback(() => {
    setSearchQuery('');
    handleSearch('');
  }, [handleSearch]);

  const handleLoadMore = useCallback(() => {
    if (!isLoadingLibrary && hasMoreLibrary) {
      loadMoreLibrary();
    }
  }, [isLoadingLibrary, hasMoreLibrary, loadMoreLibrary]);

  useEffect(() => {
    refreshLibrary();
  }, [refreshLibrary]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#F5F7FA] mb-2">
          Bibliothèque
        </h1>
        <p className="text-[#A1A8B3]">
          Découvrez et explorez les webnovels disponibles
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-8">
        <div className="relative max-w-2xl">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#6B7280]">
            <Search className="w-5 h-5" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSearch(searchQuery);
              }
            }}
            placeholder="Rechercher un novel..."
            className="w-full pl-12 pr-12 py-3 bg-[#1A1D24] border border-[#2D3139] rounded-lg text-[#F5F7FA] placeholder-[#6B7280] focus:outline-none focus:border-[#5B8CFF] focus:ring-1 focus:ring-[#5B8CFF] transition-colors"
          />
          {searchQuery && (
            <button
              onClick={handleClearSearch}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-[#6B7280] hover:text-[#F5F7FA] transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Results Count */}
      {library.length > 0 && (
        <div className="mb-6 text-sm text-[#6B7280]">
          {library.length} novel{library.length > 1 ? 's' : ''} trouvé{library.length > 1 ? 's' : ''}
        </div>
      )}

      {/* Grid */}
      {library.length > 0 ? (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6">
            {library.map((novel) => (
              <NovelCard key={novel.id} novel={novel} variant="grid" />
            ))}
          </div>

          {/* Load More */}
          {hasMoreLibrary && (
            <div className="mt-8 text-center">
              <button
                onClick={handleLoadMore}
                disabled={isLoadingLibrary}
                className="px-6 py-3 bg-[#1A1D24] border border-[#2D3139] text-[#F5F7FA] font-medium rounded-lg hover:bg-[#242830] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center space-x-2 mx-auto"
              >
                {isLoadingLibrary ? (
                  <>
                    <div className="w-5 h-5 border-2 border-[#5B8CFF] border-t-transparent rounded-full animate-spin" />
                    <span>Chargement...</span>
                  </>
                ) : (
                  <>
                    <span>Charger plus</span>
                    <ChevronDown className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          )}
        </>
      ) : isLoadingLibrary ? (
        /* Loading State */
        <div className="flex items-center justify-center py-16">
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-4 border-4 border-[#5B8CFF] border-t-transparent rounded-full animate-spin" />
            <p className="text-[#A1A8B3]">Chargement de la bibliothèque...</p>
          </div>
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-16">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-[#242830] flex items-center justify-center">
            <BookOpen className="w-8 h-8 text-[#6B7280]" />
          </div>
          <h3 className="text-lg font-medium text-[#F5F7FA] mb-2">
            Bibliothèque vide
          </h3>
          <p className="text-[#6B7280]">
            {searchQuery ? 'Aucun résultat pour cette recherche' : 'La bibliothèque est vide pour le moment'}
          </p>
        </div>
      )}
    </div>
  );
};

export default LibraryPage;