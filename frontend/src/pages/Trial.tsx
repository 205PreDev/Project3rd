import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';

export default function Trial() {
  const navigate = useNavigate();
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showExitModal, setShowExitModal] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // 이미지 미리보기
    const reader = new FileReader();
    reader.onload = () => {
      setUploadedImage(reader.result as string);
    };
    reader.readAsDataURL(file);

    // API 업로드 (워터마크 처리)
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/v1/trial/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setSessionId(data.session_id);
        setProcessedImage(data.processed_image_url);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setIsProcessing(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleSignup = () => {
    navigate('/signup');
  };

  const handleExit = () => {
    setShowExitModal(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="container mx-auto px-4 py-6 flex justify-between items-center">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>돌아가기</span>
        </button>
        <button
          onClick={handleSignup}
          className="px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-lg hover:shadow-lg transition-all"
        >
          회원가입
        </button>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Title */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              무료 체험하기
            </h1>
            <p className="text-lg text-gray-600">
              이미지를 업로드하고 AI 배경 제거를 체험해보세요
            </p>
            <div className="mt-4 inline-block bg-yellow-100 text-yellow-800 px-4 py-2 rounded-full text-sm font-medium">
              체험 모드: 워터마크가 포함됩니다
            </div>
          </div>

          {!uploadedImage ? (
            /* Upload Area */
            <div
              {...getRootProps()}
              className={`border-4 border-dashed rounded-3xl p-16 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-300 hover:border-purple-400 hover:bg-gray-50'
              }`}
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center">
                <div className="w-24 h-24 bg-gradient-to-br from-purple-100 to-blue-100 rounded-full flex items-center justify-center mb-6">
                  <svg className="w-12 h-12 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-2">
                  {isDragActive ? '여기에 놓으세요' : '이미지를 드래그하거나 클릭하세요'}
                </h3>
                <p className="text-gray-600 mb-4">
                  PNG, JPG 파일 지원 (최대 10MB)
                </p>
                <button className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all">
                  파일 선택
                </button>
              </div>
            </div>
          ) : (
            /* Processing/Result Area */
            <div className="space-y-8">
              {/* Image Comparison */}
              <div className="grid md:grid-cols-2 gap-8">
                {/* Original */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-700">원본 이미지</h3>
                  <div className="relative rounded-2xl overflow-hidden shadow-xl bg-gray-100 aspect-square">
                    <img
                      src={uploadedImage}
                      alt="Original"
                      className="w-full h-full object-contain"
                    />
                  </div>
                </div>

                {/* Processed */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-700">처리된 이미지</h3>
                  <div className="relative rounded-2xl overflow-hidden shadow-xl bg-gray-100 aspect-square">
                    {isProcessing ? (
                      <div className="w-full h-full flex flex-col items-center justify-center">
                        <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600 mb-4"></div>
                        <p className="text-gray-600 font-medium">AI가 배경을 제거하는 중...</p>
                        <p className="text-sm text-gray-500 mt-2">잠시만 기다려주세요</p>
                      </div>
                    ) : processedImage ? (
                      <>
                        <img
                          src={processedImage}
                          alt="Processed"
                          className="w-full h-full object-contain"
                        />
                        {/* Watermark */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                          <div className="transform rotate-[-30deg] text-white/30 text-4xl font-bold">
                            체험 모드
                          </div>
                        </div>
                      </>
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        처리 중...
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-4 justify-center">
                <button
                  onClick={() => {
                    setUploadedImage(null);
                    setProcessedImage(null);
                    setSessionId(null);
                  }}
                  className="px-8 py-3 bg-white border-2 border-gray-300 rounded-xl font-semibold hover:border-purple-500 hover:shadow-lg transition-all"
                >
                  다른 이미지 업로드
                </button>
                <button
                  onClick={handleSignup}
                  className="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all flex items-center gap-2"
                >
                  워터마크 없이 사용하기
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>

              {/* Info Box */}
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 border border-purple-200">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 mb-2">회원가입하면 이런 기능을 사용할 수 있어요</h4>
                    <ul className="space-y-2 text-gray-700">
                      <li className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        워터마크 없는 고화질 이미지
                      </li>
                      <li className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        다양한 배경 스타일 선택
                      </li>
                      <li className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        AI 광고 문구 자동 생성
                      </li>
                      <li className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        가입 시 10 크레딧 무료 제공
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Exit Intent Modal */}
      {showExitModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
            <h3 className="text-2xl font-bold mb-4">잠깐만요!</h3>
            <p className="text-gray-600 mb-6">
              회원가입하시면 워터마크 없이 무제한으로 이용하실 수 있어요.
              지금 가입하시겠어요?
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setShowExitModal(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition"
              >
                나중에
              </button>
              <button
                onClick={handleSignup}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold hover:shadow-lg transition"
              >
                회원가입
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
