import React, { useEffect } from 'react';
import { Clock } from 'lucide-react';
import { useApp } from '../context/AppContext';
import NovelCard from '../components/novel/NovelCard';

const HistoryPage: React.FC = () => {
  const { history, isLoadingHistory, refreshHistory } = useApp();

  useEffect(() => {
    refreshHistory();
  }, [refreshHistory]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#F5F7FA] mb-2">
          Historique
        </h1>
        <p className="text-[#A1A8B3]">
          Retrouvez les webnovels que vous avez consultés
        </p>
      </div>

      {/* Content */}
      {history.length > 0 ? (
        <>
          <div className="mb-6 text-sm text-[#6B7280]">
            {history.length} novel{history.length > 1 ? 's' : ''} dans l'historique
          </div>
          <div className="space-y-3">
            {history.map((novel) => (
              <NovelCard key={novel.id} novel={novel} variant="list" />
            ))}
          </div>
        </>
      ) : isLoadingHistory ? (
        /* Loading State */
        <div className="flex items-center justify-center py-16">
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-4 border-4 border-[#5B8CFF] border-t-transparent rounded-full animate-spin" />
            <p className="text-[#A1A8B3]">Chargement de l'historique...</p>
          </div>
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-16">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-[#242830] flex items-center justify-center">
            <Clock className="w-8 h-8 text-[#6B7280]" />
          </div>
          <h3 className="text-lg font-medium text-[#F5F7FA] mb-2">
            Historique vide
          </h3>
          <p className="text-[#6B7280]">
            Votre historique apparaîtra ici lorsque vous consulterez des novels
          </p>
        </div>
      )}
    </div>
  );
};

export default HistoryPage;