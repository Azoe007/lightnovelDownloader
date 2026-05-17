import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, Heart, Clock, Download } from 'lucide-react';
import { useApp } from '../../context/AppContext';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const { downloads } = useApp();
  
  const activeDownloads = downloads.filter(d => 
    d.status === 'downloading' || d.status === 'pending'
  );

  const navItems = [
    { path: '/', icon: Home, label: 'Accueil' },
    { path: '/library', icon: BookOpen, label: 'Bibliothèque' },
    { path: '/favorites', icon: Heart, label: 'Favoris' },
    { path: '/history', icon: Clock, label: 'Historique' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-[#0F1115]">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#1A1D24]/95 backdrop-blur-sm border-b border-[#2D3139]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#5B8CFF] to-[#8B5CF6] flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">LNCrawler</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-1">
              {navItems.map(({ path, icon: Icon, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors ${
                    isActive(path)
                      ? 'bg-[#5B8CFF]/20 text-[#5B8CFF]'
                      : 'text-[#A1A8B3] hover:text-[#F5F7FA] hover:bg-[#242830]'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{label}</span>
                </Link>
              ))}
            </nav>

            {/* Downloads indicator */}
            {activeDownloads.length > 0 && (
              <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 bg-[#5B8CFF]/20 rounded-full">
                <Download className="w-4 h-4 text-[#5B8CFF]" />
                <span className="text-sm text-[#5B8CFF] font-medium">
                  {activeDownloads.length} en cours
                </span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-[#1A1D24]/95 backdrop-blur-sm border-t border-[#2D3139]">
        <div className="flex items-center justify-around py-2">
          {navItems.map(({ path, icon: Icon, label }) => (
            <Link
              key={path}
              to={path}
              className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-lg transition-colors ${
                isActive(path)
                  ? 'text-[#5B8CFF]'
                  : 'text-[#A1A8B3]'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs font-medium">{label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-16 pb-20 md:pb-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;