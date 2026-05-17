import React, { useState, useEffect } from 'react';
import { Download, Link, RefreshCw, Inbox } from 'lucide-react';
import { useApp } from '../context/AppContext';
import DownloadCard from '../components/novel/DownloadCard';

const HomePage: React.FC = () => {
  const [url, setUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { startDownload, downloads, refreshDownloads, isLoadingDownloads } = useApp();

  const activeDownloads = downloads.filter(d => 
    d.status === 'downloading' || d.status === 'pending' || d.status === 'paused'
  );

  const completedDownloads = downloads.filter(d => 
    d.status === 'completed' || d.status === 'failed' || d.status === 'cancelled'
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsSubmitting(true);
    try {
      await startDownload(url.trim());
      setUrl('');
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    refreshDownloads();
    // Poll for updates every 5 seconds
    const interval = setInterval(refreshDownloads, 5000);
    return () => clearInterval(interval);
  }, [refreshDownloads]);

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#F5F7FA] mb-2">
          Télécharger un <span className="gradient-text">Webnovel</span>
        </h1>
        <p className="text-[#A1A8B3]">
          Collez l'URL d'un novel pour le télécharger au format EPUB
        </p>
      </div>

      {/* URL Input Form */}
      <form onSubmit={handleSubmit} className="mb-10">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#6B7280]">
              <Link className="w-5 h-5" />
            </div>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://novelfrance.fr/novel/..."
              className="w-full pl-12 pr-4 py-3 bg-[#1A1D24] border border-[#2D3139] rounded-lg text-[#F5F7FA] placeholder-[#6B7280] focus:outline-none focus:border-[#5B8CFF] focus:ring-1 focus:ring-[#5B8CFF] transition-colors"
              disabled={isSubmitting}
            />
          </div>
          <button
            type="submit"
            disabled={isSubmitting || !url.trim()}
            className="px-6 py-3 bg-gradient-to-r from-[#5B8CFF] to-[#8B5CF6] text-white font-medium rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2 min-w-[180px]"
          >
            {isSubmitting ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>En cours...</span>
              </>
            ) : (
              <>
                <Download className="w-5 h-5" />
                <span>Démarrer</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Active Downloads */}
      {activeDownloads.length > 0 && (
        <section className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-[#F5F7FA]">
              Téléchargements en cours
            </h2>
            <button
              onClick={refreshDownloads}
              className="p-2 text-[#6B7280] hover:text-[#F5F7FA] transition-colors"
            >
              <RefreshCw className={`w-5 h-5 ${isLoadingDownloads ? 'animate-spin' : ''}`} />
            </button>
          </div>
          <div className="space-y-3">
            {activeDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </div>
        </section>
      )}

      {/* Completed Downloads */}
      {completedDownloads.length > 0 && (
        <section className="mb-10">
          <h2 className="text-xl font-semibold text-[#F5F7FA] mb-4">
            Téléchargements terminés
          </h2>
          <div className="space-y-3">
            {completedDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </div>
        </section>
      )}

      {/* Empty State */}
      {downloads.length === 0 && !isLoadingDownloads && (
        <div className="text-center py-16">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-[#242830] flex items-center justify-center">
            <Inbox className="w-8 h-8 text-[#6B7280]" />
          </div>
          <h3 className="text-lg font-medium text-[#F5F7FA] mb-2">
            Aucun téléchargement
          </h3>
          <p className="text-[#6B7280]">
            Commencez par coller l'URL d'un webnovel ci-dessus
          </p>
        </div>
      )}
    </div>
  );
};

export default HomePage;