import { useState } from 'react';

interface ShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  imageUrl: string;
  caption?: string;
  imageId?: number;
}

export default function ShareModal({
  isOpen,
  onClose,
  imageUrl,
  caption = '',
  imageId,
}: ShareModalProps) {
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  if (!isOpen) return null;

  const PLATFORMS = [
    {
      id: 'instagram',
      name: 'Instagram',
      icon: '📷',
      color: 'from-pink-500 to-purple-600',
      action: 'instagram',
    },
    {
      id: 'facebook',
      name: 'Facebook',
      icon: '👍',
      color: 'from-blue-500 to-blue-700',
      action: 'facebook',
    },
    {
      id: 'kakao',
      name: 'KakaoTalk',
      icon: '💬',
      color: 'from-yellow-400 to-yellow-500',
      action: 'kakao',
    },
    {
      id: 'download',
      name: '다운로드',
      icon: '💾',
      color: 'from-gray-500 to-gray-700',
      action: 'download',
    },
  ];

  const handleShare = async (platform: string) => {
    setSelectedPlatform(platform);

    switch (platform) {
      case 'instagram':
        await handleInstagramShare();
        break;
      case 'facebook':
        await handleFacebookShare();
        break;
      case 'kakao':
        await handleKakaoShare();
        break;
      case 'download':
        await handleDownload();
        break;
    }
  };

  const handleInstagramShare = async () => {
    // Instagram은 직접 공유 API가 없으므로 클립보드 복사 + 안내
    try {
      // 이미지 다운로드 후 클립보드에 복사
      const blob = await fetch(imageUrl).then(r => r.blob());
      const item = new ClipboardItem({ 'image/png': blob });
      await navigator.clipboard.write([item]);

      // 텍스트도 클립보드에 복사
      await navigator.clipboard.writeText(caption);

      setCopied(true);
      setTimeout(() => setCopied(false), 3000);

      // Instagram 앱 열기 (모바일) 또는 웹 버전
      if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        window.location.href = 'instagram://';
      } else {
        window.open('https://www.instagram.com/', '_blank');
      }
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
      // Fallback: 다운로드만 진행
      await handleDownload();
    }
  };

  const handleFacebookShare = async () => {
    // Facebook Web Share API
    const shareUrl = encodeURIComponent(imageUrl);
    const shareText = encodeURIComponent(caption);

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI 생성 이미지',
          text: caption,
          url: imageUrl,
        });
      } catch (error) {
        console.error('Share failed:', error);
      }
    } else {
      // Fallback: Facebook Dialog
      const facebookShareUrl = `https://www.facebook.com/dialog/share?app_id=${
        import.meta.env.VITE_FACEBOOK_APP_ID || '123456789'
      }&display=popup&href=${shareUrl}&quote=${shareText}`;
      window.open(facebookShareUrl, '_blank', 'width=600,height=400');
    }
  };

  const handleKakaoShare = async () => {
    // Kakao SDK 사용
    if (typeof window !== 'undefined' && (window as any).Kakao) {
      const Kakao = (window as any).Kakao;

      if (!Kakao.isInitialized()) {
        Kakao.init(import.meta.env.VITE_KAKAO_JS_KEY);
      }

      Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: 'AI로 생성한 이미지',
          description: caption,
          imageUrl: imageUrl,
          link: {
            mobileWebUrl: window.location.origin,
            webUrl: window.location.origin,
          },
        },
        buttons: [
          {
            title: '자세히 보기',
            link: {
              mobileWebUrl: window.location.origin,
              webUrl: window.location.origin,
            },
          },
        ],
      });
    } else {
      alert('Kakao SDK를 불러오는 중입니다. 잠시 후 다시 시도해주세요.');
    }
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-image-${imageId || Date.now()}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleCopyCaption = async () => {
    await navigator.clipboard.writeText(caption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center rounded-t-3xl">
          <h2 className="text-2xl font-bold text-gray-900">SNS 공유하기</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-all"
          >
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Image Preview */}
          <div className="relative rounded-2xl overflow-hidden shadow-lg">
            <img
              src={imageUrl}
              alt="Share preview"
              className="w-full h-auto max-h-96 object-contain bg-gray-100"
            />
            {/* AI Disclosure Badge */}
            <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg">
              <div className="flex items-center gap-2 text-sm">
                <svg className="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <span className="font-medium text-gray-700">AI 제작</span>
              </div>
            </div>
          </div>

          {/* Caption */}
          {caption && (
            <div className="p-4 bg-gray-50 rounded-xl space-y-3">
              <div className="flex justify-between items-center">
                <h3 className="font-semibold text-gray-900">광고 문구</h3>
                <button
                  onClick={handleCopyCaption}
                  className="flex items-center gap-2 px-3 py-1.5 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-all text-sm"
                >
                  {copied ? (
                    <>
                      <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-green-600 font-medium">복사됨</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      <span className="text-gray-600">복사</span>
                    </>
                  )}
                </button>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{caption}</p>
            </div>
          )}

          {/* Platform Buttons */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-900">플랫폼 선택</h3>
            <div className="grid grid-cols-2 gap-3">
              {PLATFORMS.map((platform) => (
                <button
                  key={platform.id}
                  onClick={() => handleShare(platform.action)}
                  disabled={isDownloading && platform.action === 'download'}
                  className={`relative p-6 rounded-xl bg-gradient-to-r ${platform.color} text-white hover:shadow-xl hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  <div className="flex flex-col items-center gap-2">
                    <span className="text-4xl">{platform.icon}</span>
                    <span className="font-semibold">
                      {isDownloading && platform.action === 'download'
                        ? '다운로드 중...'
                        : platform.name}
                    </span>
                  </div>
                  {selectedPlatform === platform.action && (
                    <div className="absolute top-2 right-2 w-6 h-6 bg-white rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* AI Transparency Notice */}
          <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-800">
                <p className="font-semibold mb-1">AI 제작 콘텐츠 표시</p>
                <p className="text-blue-700">
                  이 이미지는 AI로 생성되었습니다. 일부 플랫폼에서는 AI 생성 콘텐츠임을 명시해야 할 수 있습니다.
                </p>
              </div>
            </div>
          </div>

          {/* Platform-specific Instructions */}
          {selectedPlatform === 'instagram' && (
            <div className="p-4 bg-purple-50 rounded-xl border border-purple-200 animate-fadeIn">
              <h4 className="font-semibold text-purple-900 mb-2">Instagram 공유 방법</h4>
              <ol className="space-y-2 text-sm text-purple-800">
                <li className="flex items-start gap-2">
                  <span className="font-bold">1.</span>
                  <span>이미지와 문구가 클립보드에 복사되었습니다</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold">2.</span>
                  <span>Instagram 앱을 열고 새 게시물을 작성하세요</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold">3.</span>
                  <span>갤러리에서 다운로드된 이미지를 선택하세요</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="font-bold">4.</span>
                  <span>문구 입력란에서 붙여넣기(Ctrl+V)를 하세요</span>
                </li>
              </ol>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 rounded-b-3xl">
          <button
            onClick={onClose}
            className="w-full px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  );
}
