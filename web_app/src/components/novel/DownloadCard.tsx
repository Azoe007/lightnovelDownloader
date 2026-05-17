import React from 'react';
import type { DownloadTask } from '../../types';
import { Pause, Play, X, CheckCircle, AlertCircle, Clock } from 'lucide-react';
import { useApp } from '../../context/AppContext';

interface DownloadCardProps {
  download: DownloadTask;
}

const DownloadCard: React.FC<DownloadCardProps> = ({ download }) => {
  const { pauseDownload, resumeDownload, cancelDownload } = useApp();

  const getStatusConfig = () => {
    switch (download.status) {
      case 'downloading':
        return {
          color: 'text-[#5B8CFF]',
          bgColor: 'bg-[#5B8CFF]/20',
          borderColor: 'border-[#5B8CFF]/30',
          icon: <Clock className="w-4 h-4 animate-pulse" />,
          label: 'En cours',
        };
      case 'paused':
        return {
          color: 'text-[#F59E0B]',
          bgColor: 'bg-[#F59E0B]/20',
          borderColor: 'border-[#F59E0B]/30',
          icon: <Pause className="w-4 h-4" />,
          label: 'En pause',
        };
      case 'completed':
        return {
          color: 'text-[#22C55E]',
          bgColor: 'bg-[#22C55E]/20',
          borderColor: 'border-[#22C55E]/30',
          icon: <CheckCircle className="w-4 h-4" />,
          label: 'Terminé',
        };
      case 'failed':
        return {
          color: 'text-[#EF4444]',
          bgColor: 'bg-[#EF4444]/20',
          borderColor: 'border-[#EF4444]/30',
          icon: <AlertCircle className="w-4 h-4" />,
          label: 'Échoué',
        };
      case 'pending':
        return {
          color: 'text-[#3B82F6]',
          bgColor: 'bg-[#3B82F6]/20',
          borderColor: 'border-[#3B82F6]/30',
          icon: <Clock className="w-4 h-4" />,
          label: 'En attente',
        };
      default:
        return {
          color: 'text-[#6B7280]',
          bgColor: 'bg-[#6B7280]/20',
          borderColor: 'border-[#6B7280]/30',
          icon: null,
          label: download.status,
        };
    }
  };

  const status = getStatusConfig();

  return (
    <div className={`bg-[#1A1D24] rounded-lg p-4 border ${status.borderColor} fade-in`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-[#F5F7FA] line-clamp-1" title={download.novel_title}>
            {download.novel_title}
          </h3>
          <div className="flex items-center mt-1">
            <span className={`flex items-center space-x-1 text-xs px-2 py-0.5 rounded-full ${status.bgColor} ${status.color}`}>
              {status.icon}
              <span>{status.label}</span>
            </span>
          </div>
        </div>
      </div>

      {/* Progress */}
      {(download.status === 'downloading' || download.status === 'pending') && (
        <div className="mb-3">
          <div className="flex items-center justify-between text-xs text-[#A1A8B3] mb-2">
            <span>Chapitre {download.current_chapter} / {download.total_chapters}</span>
            <span>{download.progress}%</span>
          </div>
          <div className="w-full h-2 bg-[#242830] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#5B8CFF] to-[#8B5CF6] rounded-full transition-all duration-300"
              style={{ width: `${download.progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Actions */}
      {(download.status === 'downloading' || download.status === 'paused' || download.status === 'pending') && (
        <div className="flex items-center space-x-2">
          {download.status === 'downloading' ? (
            <button
              onClick={() => pauseDownload(download.id)}
              className="flex items-center space-x-1 px-3 py-1.5 text-xs font-medium text-[#F59E0B] bg-[#F59E0B]/10 rounded-lg hover:bg-[#F59E0B]/20 transition-colors"
            >
              <Pause className="w-3 h-3" />
              <span>Pause</span>
            </button>
          ) : (
            <button
              onClick={() => resumeDownload(download.id)}
              className="flex items-center space-x-1 px-3 py-1.5 text-xs font-medium text-[#5B8CFF] bg-[#5B8CFF]/10 rounded-lg hover:bg-[#5B8CFF]/20 transition-colors"
            >
              <Play className="w-3 h-3" />
              <span>Reprendre</span>
            </button>
          )}
          <button
            onClick={() => cancelDownload(download.id)}
            className="flex items-center space-x-1 px-3 py-1.5 text-xs font-medium text-[#EF4444] bg-[#EF4444]/10 rounded-lg hover:bg-[#EF4444]/20 transition-colors"
          >
            <X className="w-3 h-3" />
            <span>Annuler</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default DownloadCard;