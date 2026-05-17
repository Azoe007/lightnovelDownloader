import React, { useEffect } from 'react';
import { Heart } from 'lucide-react';
import { useApp } from '../context/AppContext';
import NovelCard from '../components/novel/NovelCard';

const FavoritesPage: React.FC = () => {
  const { favorites, isLoadingFavorites, refreshFavorites } = useApp();

  useEffect(() => {
    refreshFavorites();
  }, [refreshFavorites]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#F5F7FA] mb-2">
          Mes Favoris
        </h1>
        <p className="text-[#A1A8B3]">
          Retrouvez tous vos webnovels préférés
        </p>
      </div>

      {/* Content */}
      {favorites.length > 0 ? (
        <>
          <div className="mb-6 text-sm text-[#6B7280]">
            {favorites.length} favori{favorites.length > 1 ? 's' : ''}
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6">
            {favorites.map((novel) => (
              <NovelCard key={novel.id} novel={novel} variant="grid" />
            ))}
          </div>
        </>
      ) : isLoadingFavorites ? (
        /* Loading State */
        <div className="flex items-center justify-center py-16">
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-4 border-4 border-[#5B8CFF] border-t-transparent rounded-full animate-spin" />
            <p className="text-[#A1A8B3]">Chargement des favoris...</p>
          </div>
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-16">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-[#242830] flex items-center justify-center">
            <Heart className="w-8 h-8 text-[#6B7280]" />
          </div>
          <h3 className="text-lg font-medium text-[#F5F7FA] mb-2">
            Aucun favori
          </h3>
          <p className="text-[#6B7280]">
            Ajoutez des novels à vos favoris en cliquant sur le cœur
          </p>
        </div>
      )}
    </div>
  );
};

export default FavoritesPage;