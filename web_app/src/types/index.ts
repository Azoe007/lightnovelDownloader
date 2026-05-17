export interface Novel {
  id: number;
  title: string;
  slug: string;
  author: string | null;
  description: string | null;
  cover_url: string | null;
  cover_path: string | null;
  source_url: string;
  source_site: string;
  total_chapters: number;
  language: string;
  created_at: string;
  updated_at: string;
}

export interface DownloadTask {
  id: number;
  novel_id: number;
  novel_title: string;
  status: 'pending' | 'downloading' | 'paused' | 'completed' | 'failed' | 'cancelled';
  current_chapter: number;
  total_chapters: number;
  progress: number;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface DownloadProgress {
  currentChapter: number;
  totalChapters: number;
  progress: number;
  eta?: string;
}