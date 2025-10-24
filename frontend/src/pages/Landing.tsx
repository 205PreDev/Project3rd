import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SAMPLE_IMAGES = [
  {
    before: '/samples/before-1.jpg',
    after: '/samples/after-1.jpg',
    caption: '패션 상품 배경 교체',
  },
  {
    before: '/samples/before-2.jpg',
    after: '/samples/after-2.jpg',
    caption: '음식 사진 배경 변경',
  },
  {
    before: '/samples/before-3.jpg',
    after: '/samples/after-3.jpg',
    caption: '제품 사진 전문화',
  },
];

export default function Landing() {
  const navigate = useNavigate();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [sliderPosition, setSliderPosition] = useState(50);

  const handleStartTrial = () => {
    navigate('/trial');
  };

  const handleSignup = () => {
    navigate('/signup');
  };

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % SAMPLE_IMAGES.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + SAMPLE_IMAGES.length) % SAMPLE_IMAGES.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Hero Section */}
      <header className="container mx-auto px-4 py-8">
        <nav className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg"></div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              AI 이미지 생성
            </span>
          </div>
          <button
            onClick={handleSignup}
            className="px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-lg hover:shadow-lg transition-all"
          >
            시작하기
          </button>
        </nav>
      </header>

      {/* Main Hero */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 bg-clip-text text-transparent">
          AI로 상품 사진을
          <br />
          전문가처럼 만들기
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          배경 제거, 새로운 배경 합성, SNS 광고 문구까지
          <br />
          단 몇 초만에 완성하세요
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={handleStartTrial}
            className="px-8 py-4 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-lg font-semibold rounded-xl hover:shadow-2xl hover:scale-105 transition-all"
          >
            무료로 체험하기
          </button>
          <button
            onClick={() => document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' })}
            className="px-8 py-4 bg-white text-gray-700 text-lg font-semibold rounded-xl border-2 border-gray-200 hover:border-purple-500 hover:shadow-lg transition-all"
          >
            둘러보기
          </button>
        </div>
      </section>

      {/* Before/After Slider Demo */}
      <section id="demo" className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-12">
          변화를 직접 확인하세요
        </h2>

        <div className="max-w-4xl mx-auto">
          {/* Image Comparison Slider */}
          <div className="relative rounded-2xl overflow-hidden shadow-2xl mb-8">
            <div className="relative w-full h-96 bg-gray-100">
              {/* Before Image */}
              <div className="absolute inset-0">
                <img
                  src={SAMPLE_IMAGES[currentSlide].before}
                  alt="Before"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://via.placeholder.com/800x600?text=Before';
                  }}
                />
                <div className="absolute top-4 left-4 bg-black/70 text-white px-4 py-2 rounded-lg font-semibold">
                  Before
                </div>
              </div>

              {/* After Image with Slider */}
              <div
                className="absolute inset-0"
                style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
              >
                <img
                  src={SAMPLE_IMAGES[currentSlide].after}
                  alt="After"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://via.placeholder.com/800x600?text=After';
                  }}
                />
                <div className="absolute top-4 right-4 bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold">
                  After
                </div>
              </div>

              {/* Slider Handle */}
              <div
                className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize shadow-lg"
                style={{ left: `${sliderPosition}%` }}
                onMouseDown={(e) => {
                  const container = e.currentTarget.parentElement;
                  if (!container) return;

                  const handleMove = (moveEvent: MouseEvent) => {
                    const rect = container.getBoundingClientRect();
                    const x = moveEvent.clientX - rect.left;
                    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
                    setSliderPosition(percentage);
                  };

                  const handleUp = () => {
                    document.removeEventListener('mousemove', handleMove);
                    document.removeEventListener('mouseup', handleUp);
                  };

                  document.addEventListener('mousemove', handleMove);
                  document.addEventListener('mouseup', handleUp);
                }}
              >
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-white rounded-full shadow-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Caption */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur-sm px-6 py-3 rounded-full shadow-lg">
              <p className="text-gray-800 font-medium">{SAMPLE_IMAGES[currentSlide].caption}</p>
            </div>
          </div>

          {/* Slider Controls */}
          <div className="flex justify-center items-center gap-4">
            <button
              onClick={prevSlide}
              className="p-3 bg-white rounded-full shadow-lg hover:bg-gray-50 transition-all"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div className="flex gap-2">
              {SAMPLE_IMAGES.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentSlide ? 'bg-purple-600 w-8' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
            <button
              onClick={nextSlide}
              className="p-3 bg-white rounded-full shadow-lg hover:bg-gray-50 transition-all"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20 bg-white/50 rounded-3xl my-20">
        <h2 className="text-4xl font-bold text-center mb-16">
          이런 기능들이 포함되어 있어요
        </h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="text-center p-8 rounded-2xl bg-white shadow-lg hover:shadow-xl transition-all">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3">AI 배경 제거</h3>
            <p className="text-gray-600">
              클릭 한 번으로 상품만 깔끔하게 추출합니다
            </p>
          </div>

          <div className="text-center p-8 rounded-2xl bg-white shadow-lg hover:shadow-xl transition-all">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3">배경 스타일 선택</h3>
            <p className="text-gray-600">
              수백 가지 전문 배경 중 마음에 드는 것을 선택하세요
            </p>
          </div>

          <div className="text-center p-8 rounded-2xl bg-white shadow-lg hover:shadow-xl transition-all">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3">SNS 광고 문구</h3>
            <p className="text-gray-600">
              AI가 플랫폼별 최적화된 광고 문구를 생성해드려요
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-3xl mx-auto bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl p-12 text-white shadow-2xl">
          <h2 className="text-4xl font-bold mb-4">
            지금 바로 시작하세요
          </h2>
          <p className="text-xl mb-8 text-purple-100">
            회원가입 시 10 크레딧 무료 제공
          </p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={handleStartTrial}
              className="px-8 py-4 bg-white text-purple-600 text-lg font-semibold rounded-xl hover:bg-gray-100 hover:shadow-xl transition-all"
            >
              무료 체험하기
            </button>
            <button
              onClick={handleSignup}
              className="px-8 py-4 bg-purple-700 text-white text-lg font-semibold rounded-xl border-2 border-purple-300 hover:bg-purple-800 transition-all"
            >
              회원가입
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-12 border-t border-gray-200">
        <div className="text-center text-gray-600">
          <p>&copy; 2025 AI 이미지 생성. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
