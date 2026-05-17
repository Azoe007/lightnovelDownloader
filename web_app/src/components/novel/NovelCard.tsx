import React from 'react';
import type { Novel } from '../../types';
import { Heart, Book } from 'lucide-react';
import { useApp } from '../../context/AppContext';

interface NovelCardProps {
  novel: Novel;
  showActions?: boolean;
  variant?: 'grid' | 'list';
}

const NovelCard: React.FC<NovelCardProps> = ({ 
  novel, 
  showActions = true, 
  variant = 'grid' 
}) => {
  const { toggleFavorite, isFavorite } = useApp();
  const favorite = isFavorite(novel.id);

  if (variant === 'list') {
    return (
      <div className="bg-[#1A1D24] rounded-lg overflow-hidden hover:bg-[#242830] transition-colors fade-in">
        <div className="flex p-4">
          {/* Cover */}
          <div className="w-20 h-28 flex-shrink-0 rounded-md overflow-hidden bg-[#242830]">
            {novel.cover_url ? (
              <img
                src={novel.cover_url}
                alt={novel.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <Book className="w-8 h-8 text-[#6B7280]" />
              </div>
            )}
          </div>

          {/* Info */}
          <div className="ml-4 flex-1 min-w-0">
            <h3 className="font-semibold text-[#F5F7FA] line-clamp-2" title={novel.title}>
              {novel.title}
            </h3>
            {novel.author && (
              <p className="text-sm text-[#A1A8B3] mt-1 line-clamp-1">
                {novel.author}
              </p>
            )}
            <div className="flex items-center mt-2 text-xs text-[#6B7280]">
              <span>{novel.total_chapters} chapitres</span>
              <span className="mx-2">•</span>
              <span className="uppercase">{novel.language}</span>
            </div>
          </div>

          {/* Actions */}
          {showActions && (
            <div className="flex items-center">
              <button
                onClick={() => toggleFavorite(novel)}
                className={`p-2 rounded-lg transition-colors ${
                  favorite 
                    ? 'text-[#EF4444] bg-[#EF4444]/10' 
                    : 'text-[#6B7280] hover:text-[#EF4444] hover:bg-[#EF4444]/10'
                }`}
                title={favorite ? 'Retirer des favoris' : 'Ajouter aux favoris'}
              >
                <Heart className="w-5 h-5" fill={favorite ? 'currentColor' : 'none'} />
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Grid variant
  return (
    <div className="bg-[#1A1D24] rounded-lg overflow-hidden hover:bg-[#242830] transition-colors fade-in group">
      {/* Cover */}
      <div className="relative aspect-[2/3] bg-[#242830] overflow-hidden">
        {novel.cover_url ? (
          <img
            src={novel.cover_url}
            alt={novel.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
            }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Book className="w-12 h-12 text-[#6B7280]" />
          </div>
        )}
        
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
        
        {/* Favorite button */}
        {showActions && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleFavorite(novel);
            }}
            className={`absolute top-2 right-2 p-2 rounded-full backdrop-blur-sm transition-all ${
              favorite 
                ? 'bg-[#EF4444]/80 text-white' 
                : 'bg-black/40 text-white hover:bg-[#EF4444]/80'
            }`}
          >
            <Heart className="w-4 h-4" fill={favorite ? 'currentColor' : 'none'} />
          </button>
        )}
      </div>

      {/* Info */}
      <div className="p-3">
        <h3 className="font-semibold text-[#F5F7FA] text-sm line-clamp-2" title={novel.title}>
          {novel.title}
        </h3>
        {novel.author && (
          <p className="text-xs text-[#A1A8B3] mt-1 line-clamp-1">
            {novel.author}
          </p>
        )}
        <div className="flex items-center mt-2 text-xs text-[#6B7280]">
          <span>{novel.total_chapters} ch.</span>
        </div>
      </div>
    </div>
  );
};

export default NovelCard;