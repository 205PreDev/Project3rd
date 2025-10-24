import { useState } from 'react';

interface CaptionOption {
  id: number;
  text: string;
  platform: string;
}

interface CaptionGeneratorProps {
  imageId: number;
  productDescription?: string;
  onCaptionGenerated?: (caption: string) => void;
}

export default function CaptionGenerator({
  imageId,
  productDescription,
  onCaptionGenerated,
}: CaptionGeneratorProps) {
  const [platform, setPlatform] = useState<'instagram' | 'facebook' | 'kakao'>('instagram');
  const [style, setStyle] = useState<'engaging' | 'question' | 'concise'>('engaging');
  const [mood, setMood] = useState('');
  const [includeEmoji, setIncludeEmoji] = useState(true);
  const [includeHashtags, setIncludeHashtags] = useState(true);
  const [maxLength, setMaxLength] = useState(100);

  const [captions, setCaptions] = useState<CaptionOption[]>([]);
  const [hashtags, setHashtags] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedCaption, setSelectedCaption] = useState<number | null>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const PLATFORMS = [
    { id: 'instagram', name: 'Instagram', icon: '📷', color: 'from-pink-500 to-purple-500' },
    { id: 'facebook', name: 'Facebook', icon: '👍', color: 'from-blue-500 to-blue-600' },
    { id: 'kakao', name: 'Kakao', icon: '💬', color: 'from-yellow-400 to-yellow-500' },
  ];

  const STYLES = [
    { id: 'engaging', name: '감성형', description: '감정에 호소하는 스타일', icon: '💖' },
    { id: 'question', name: '질문형', description: '호기심을 유발하는 질문', icon: '❓' },
    { id: 'concise', name: '간결형', description: '짧고 강렬한 메시지', icon: '⚡' },
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch('/api/v1/captions/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          image_id: imageId,
          product_description: productDescription,
          platform,
          style,
          mood: mood || undefined,
          max_length: maxLength,
          include_emoji: includeEmoji,
          include_hashtags: includeHashtags,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const captionOptions: CaptionOption[] = data.captions.map((text: string, index: number) => ({
          id: index + 1,
          text,
          platform,
        }));
        setCaptions(captionOptions);
        setHashtags(data.hashtags || []);
      }
    } catch (error) {
      console.error('Failed to generate captions:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = async (caption: CaptionOption) => {
    const fullText = includeHashtags && hashtags.length > 0
      ? `${caption.text}\n\n${hashtags.map(tag => `#${tag}`).join(' ')}`
      : caption.text;

    await navigator.clipboard.writeText(fullText);
    setCopiedId(caption.id);
    setTimeout(() => setCopiedId(null), 2000);
    onCaptionGenerated?.(fullText);
  };

  return (
    <div className="w-full space-y-6">
      {/* Settings Panel */}
      <div className="bg-white rounded-2xl shadow-lg p-6 space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">광고 문구 생성</h2>

        {/* Platform Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            플랫폼 선택
          </label>
          <div className="grid grid-cols-3 gap-3">
            {PLATFORMS.map((p) => (
              <button
                key={p.id}
                onClick={() => setPlatform(p.id as any)}
                className={`p-4 rounded-xl border-2 transition-all ${
                  platform === p.id
                    ? `bg-gradient-to-r ${p.color} text-white border-transparent shadow-lg scale-105`
                    : 'bg-white border-gray-300 hover:border-gray-400'
                }`}
              >
                <div className="text-2xl mb-1">{p.icon}</div>
                <div className="font-semibold text-sm">{p.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Style Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            스타일 선택
          </label>
          <div className="space-y-2">
            {STYLES.map((s) => (
              <button
                key={s.id}
                onClick={() => setStyle(s.id as any)}
                className={`w-full p-4 rounded-xl border-2 text-left transition-all ${
                  style === s.id
                    ? 'bg-purple-50 border-purple-500'
                    : 'bg-white border-gray-300 hover:border-purple-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{s.icon}</span>
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900">{s.name}</div>
                    <div className="text-sm text-gray-600">{s.description}</div>
                  </div>
                  {style === s.id && (
                    <svg className="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Advanced Options */}
        <div className="space-y-4 p-4 bg-gray-50 rounded-xl">
          <h3 className="font-semibold text-gray-900">고급 옵션</h3>

          {/* Mood */}
          <div>
            <label htmlFor="mood" className="block text-sm font-medium text-gray-700 mb-2">
              분위기 (선택)
            </label>
            <input
              id="mood"
              type="text"
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              placeholder="예: 밝고 경쾌한, 럭셔리한, 캐주얼한"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
            />
          </div>

          {/* Max Length */}
          <div>
            <label htmlFor="maxLength" className="block text-sm font-medium text-gray-700 mb-2">
              최대 글자 수: {maxLength}자
            </label>
            <input
              id="maxLength"
              type="range"
              min="50"
              max="200"
              value={maxLength}
              onChange={(e) => setMaxLength(Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Checkboxes */}
          <div className="space-y-2">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={includeEmoji}
                onChange={(e) => setIncludeEmoji(e.target.checked)}
                className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
              />
              <span className="text-sm font-medium text-gray-700">이모지 포함</span>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={includeHashtags}
                onChange={(e) => setIncludeHashtags(e.target.checked)}
                className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
              />
              <span className="text-sm font-medium text-gray-700">해시태그 생성</span>
            </label>
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full px-6 py-4 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-xl hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center gap-2">
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              생성 중...
            </span>
          ) : (
            '광고 문구 생성하기'
          )}
        </button>
      </div>

      {/* Generated Captions */}
      {captions.length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg p-6 space-y-4">
          <h3 className="text-xl font-bold text-gray-900">생성된 광고 문구</h3>

          {captions.map((caption) => (
            <div
              key={caption.id}
              className={`p-4 rounded-xl border-2 transition-all ${
                selectedCaption === caption.id
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-200 hover:border-purple-300'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded">
                      옵션 {caption.id}
                    </span>
                  </div>
                  <p className="text-gray-900 whitespace-pre-wrap">{caption.text}</p>
                </div>
                <button
                  onClick={() => handleCopy(caption)}
                  className="flex-shrink-0 p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all"
                  title="복사"
                >
                  {copiedId === caption.id ? (
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
          ))}

          {/* Hashtags */}
          {hashtags.length > 0 && (
            <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
              <h4 className="font-semibold text-gray-900 mb-2">추천 해시태그</h4>
              <div className="flex flex-wrap gap-2">
                {hashtags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
