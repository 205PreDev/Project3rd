import { useState, useEffect } from 'react';

interface BackgroundStyle {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
  category: string;
  preview?: string;
}

interface StyleSelectorProps {
  onSelectStyle: (styleId: string, styleUrl?: string) => void;
  selectedStyle?: string;
  imageAnalysis?: {
    category?: string;
    colors?: string[];
    mood?: string;
  };
}

export default function StyleSelector({
  onSelectStyle,
  selectedStyle,
  imageAnalysis,
}: StyleSelectorProps) {
  const [activeTab, setActiveTab] = useState<string>('all');
  const [styles, setStyles] = useState<BackgroundStyle[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showPreview, setShowPreview] = useState<string | null>(null);

  const CATEGORIES = [
    { id: 'all', name: '전체', icon: '🎨' },
    { id: 'minimal', name: '미니멀', icon: '⚪' },
    { id: 'gradient', name: '그라데이션', icon: '🌈' },
    { id: 'natural', name: '자연', icon: '🌿' },
    { id: 'studio', name: '스튜디오', icon: '📸' },
    { id: 'texture', name: '텍스처', icon: '🎭' },
  ];

  // Mock styles data
  const MOCK_STYLES: BackgroundStyle[] = [
    {
      id: 'minimal-white',
      name: '화이트',
      description: '깔끔한 순백색 배경',
      thumbnail: 'https://via.placeholder.com/200x150/FFFFFF/CCCCCC?text=White',
      category: 'minimal',
    },
    {
      id: 'minimal-gray',
      name: '그레이',
      description: '중성적인 회색 배경',
      thumbnail: 'https://via.placeholder.com/200x150/F5F5F5/999999?text=Gray',
      category: 'minimal',
    },
    {
      id: 'gradient-purple',
      name: '퍼플 그라데이션',
      description: '세련된 보라색 그라데이션',
      thumbnail: 'https://via.placeholder.com/200x150/9333EA/6B21A8?text=Purple',
      category: 'gradient',
    },
    {
      id: 'gradient-blue',
      name: '블루 그라데이션',
      description: '시원한 파란색 그라데이션',
      thumbnail: 'https://via.placeholder.com/200x150/3B82F6/1D4ED8?text=Blue',
      category: 'gradient',
    },
    {
      id: 'natural-wood',
      name: '우드',
      description: '따뜻한 나무 질감',
      thumbnail: 'https://via.placeholder.com/200x150/8B4513/654321?text=Wood',
      category: 'natural',
    },
    {
      id: 'natural-marble',
      name: '마블',
      description: '고급스러운 대리석',
      thumbnail: 'https://via.placeholder.com/200x150/E5E7EB/9CA3AF?text=Marble',
      category: 'natural',
    },
    {
      id: 'studio-soft',
      name: '소프트 라이트',
      description: '부드러운 스튜디오 조명',
      thumbnail: 'https://via.placeholder.com/200x150/FEF3C7/FDE68A?text=Soft',
      category: 'studio',
    },
    {
      id: 'studio-dramatic',
      name: '드라마틱',
      description: '강렬한 조명 효과',
      thumbnail: 'https://via.placeholder.com/200x150/1F2937/111827?text=Dark',
      category: 'studio',
    },
  ];

  useEffect(() => {
    setStyles(MOCK_STYLES);
  }, []);

  const filteredStyles =
    activeTab === 'all'
      ? styles
      : styles.filter((style) => style.category === activeTab);

  // AI 추천 스타일 (이미지 분석 결과 기반)
  const recommendedStyles = imageAnalysis
    ? styles.filter((style) => {
        // 카테고리 매칭
        if (imageAnalysis.category === 'fashion' && style.category === 'minimal') return true;
        if (imageAnalysis.category === 'food' && style.category === 'natural') return true;
        if (imageAnalysis.category === 'tech' && style.category === 'gradient') return true;
        return false;
      }).slice(0, 3)
    : [];

  return (
    <div className="w-full">
      {/* AI Recommendations */}
      {recommendedStyles.length > 0 && (
        <div className="mb-8 p-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl border border-purple-200">
          <div className="flex items-center gap-2 mb-4">
            <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <h3 className="text-lg font-bold text-gray-900">AI 추천 배경</h3>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {recommendedStyles.map((style) => (
              <button
                key={style.id}
                onClick={() => onSelectStyle(style.id)}
                className={`relative rounded-xl overflow-hidden transition-all hover:scale-105 ${
                  selectedStyle === style.id
                    ? 'ring-4 ring-purple-500 shadow-xl'
                    : 'hover:shadow-lg'
                }`}
              >
                <img
                  src={style.thumbnail}
                  alt={style.name}
                  className="w-full aspect-video object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-3">
                  <p className="text-white font-semibold text-sm">{style.name}</p>
                </div>
                {selectedStyle === style.id && (
                  <div className="absolute top-2 right-2 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Category Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {CATEGORIES.map((category) => (
          <button
            key={category.id}
            onClick={() => setActiveTab(category.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl font-semibold whitespace-nowrap transition-all ${
              activeTab === category.id
                ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <span>{category.icon}</span>
            <span>{category.name}</span>
          </button>
        ))}
      </div>

      {/* Style Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {filteredStyles.map((style) => (
          <button
            key={style.id}
            onClick={() => onSelectStyle(style.id)}
            onMouseEnter={() => setShowPreview(style.id)}
            onMouseLeave={() => setShowPreview(null)}
            className={`group relative rounded-2xl overflow-hidden transition-all ${
              selectedStyle === style.id
                ? 'ring-4 ring-purple-500 shadow-2xl scale-105'
                : 'hover:shadow-xl hover:scale-105'
            }`}
          >
            {/* Thumbnail */}
            <div className="aspect-square">
              <img
                src={style.thumbnail}
                alt={style.name}
                className="w-full h-full object-cover"
              />
            </div>

            {/* Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="absolute bottom-0 left-0 right-0 p-4">
                <p className="text-white font-bold">{style.name}</p>
                <p className="text-white/80 text-xs">{style.description}</p>
              </div>
            </div>

            {/* Selected Indicator */}
            {selectedStyle === style.id && (
              <div className="absolute top-3 right-3 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center shadow-lg">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}

            {/* Preview Badge */}
            {showPreview === style.id && selectedStyle !== style.id && (
              <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold text-gray-700">
                미리보기
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Empty State */}
      {filteredStyles.length === 0 && (
        <div className="text-center py-12">
          <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <p className="text-gray-600 font-medium">스타일을 불러오는 중...</p>
        </div>
      )}

      {/* Custom Background Option */}
      <div className="mt-6 p-4 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 hover:border-purple-400 hover:bg-purple-50 transition-all">
        <button
          onClick={() => {
            // Open custom background upload modal
            console.log('Open custom background upload');
          }}
          className="w-full flex items-center justify-center gap-3 py-3"
        >
          <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span className="font-semibold text-purple-600">커스텀 배경 업로드</span>
        </button>
      </div>
    </div>
  );
}
