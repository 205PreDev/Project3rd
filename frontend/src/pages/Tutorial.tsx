import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TutorialStep from '../components/Tutorial/TutorialStep';

export default function Tutorial() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  // Tutorial state
  const [projectName, setProjectName] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const STYLES = [
    { id: 'minimal', name: '미니멀', preview: '🎨' },
    { id: 'gradient', name: '그라데이션', preview: '🌈' },
    { id: 'natural', name: '자연', preview: '🌿' },
    { id: 'studio', name: '스튜디오', preview: '📸' },
    { id: 'vintage', name: '빈티지', preview: '📜' },
  ];

  const handleCompleteStep = (step: number) => {
    if (!completedSteps.includes(step)) {
      setCompletedSteps([...completedSteps, step]);
      if (step < 3) {
        setCurrentStep(step + 1);
      }
    }
  };

  const handleCreateProject = () => {
    if (projectName.trim()) {
      handleCompleteStep(1);
    }
  };

  const handleSelectStyle = (styleId: string) => {
    setSelectedStyle(styleId);
    handleCompleteStep(2);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setUploadedImage(reader.result as string);
        handleCompleteStep(3);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFinishTutorial = () => {
    navigate('/dashboard');
  };

  const progress = (completedSteps.length / 3) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg"></div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              AI 이미지 생성
            </span>
          </div>
          <button
            onClick={() => navigate('/dashboard')}
            className="text-gray-600 hover:text-gray-900 transition"
          >
            건너뛰기
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          {/* Title */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              시작 가이드
            </h1>
            <p className="text-lg text-gray-600">
              3단계만 따라하시면 준비 완료!
            </p>
          </div>

          {/* Progress Bar */}
          <div className="mb-12">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>진행률</span>
              <span className="font-semibold">{Math.round(progress)}%</span>
            </div>
            <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-500 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>

          {/* Tutorial Steps */}
          <div className="space-y-12">
            {/* Step 1: Create Project */}
            <TutorialStep
              step={1}
              title="프로젝트 만들기"
              description="프로젝트 이름을 입력해주세요"
              isActive={currentStep === 1}
              isCompleted={completedSteps.includes(1)}
            >
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <div className="space-y-4">
                  <div>
                    <label htmlFor="projectName" className="block text-sm font-medium text-gray-700 mb-2">
                      프로젝트 이름
                    </label>
                    <input
                      id="projectName"
                      type="text"
                      value={projectName}
                      onChange={(e) => setProjectName(e.target.value)}
                      placeholder="예: 봄 신상품 컬렉션"
                      className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
                      disabled={completedSteps.includes(1)}
                    />
                  </div>
                  {!completedSteps.includes(1) && (
                    <button
                      onClick={handleCreateProject}
                      disabled={!projectName.trim()}
                      className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-xl hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                      프로젝트 생성
                    </button>
                  )}
                  {completedSteps.includes(1) && (
                    <div className="flex items-center gap-2 text-green-600">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="font-semibold">완료!</span>
                    </div>
                  )}
                </div>
              </div>
            </TutorialStep>

            {/* Step 2: Select Background Style */}
            <TutorialStep
              step={2}
              title="배경 스타일 선택"
              description="원하는 배경 스타일을 선택해주세요"
              isActive={currentStep === 2}
              isCompleted={completedSteps.includes(2)}
            >
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <div className="grid grid-cols-5 gap-4 mb-6">
                  {STYLES.map((style) => (
                    <button
                      key={style.id}
                      onClick={() => handleSelectStyle(style.id)}
                      disabled={completedSteps.includes(2)}
                      className={`aspect-square rounded-xl flex flex-col items-center justify-center gap-2 transition-all ${
                        selectedStyle === style.id
                          ? 'bg-gradient-to-br from-purple-500 to-blue-500 text-white shadow-lg scale-105'
                          : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                      } ${completedSteps.includes(2) ? 'cursor-default' : 'cursor-pointer'}`}
                    >
                      <span className="text-3xl">{style.preview}</span>
                      <span className="text-xs font-medium">{style.name}</span>
                    </button>
                  ))}
                </div>
                {completedSteps.includes(2) && (
                  <div className="flex items-center gap-2 text-green-600">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="font-semibold">스타일이 선택되었습니다!</span>
                  </div>
                )}
              </div>
            </TutorialStep>

            {/* Step 3: Upload Image */}
            <TutorialStep
              step={3}
              title="이미지 업로드"
              description="상품 이미지를 업로드해주세요"
              isActive={currentStep === 3}
              isCompleted={completedSteps.includes(3)}
            >
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                {!uploadedImage ? (
                  <label className="block cursor-pointer">
                    <div className="border-4 border-dashed border-gray-300 rounded-2xl p-12 text-center hover:border-purple-400 hover:bg-purple-50 transition-all">
                      <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-bold mb-2">이미지를 선택하세요</h3>
                      <p className="text-gray-600 text-sm">PNG, JPG (최대 10MB)</p>
                    </div>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      disabled={completedSteps.includes(3)}
                    />
                  </label>
                ) : (
                  <div className="space-y-4">
                    <div className="rounded-2xl overflow-hidden">
                      <img src={uploadedImage} alt="Uploaded" className="w-full h-64 object-cover" />
                    </div>
                    <div className="flex items-center gap-2 text-green-600">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="font-semibold">이미지가 업로드되었습니다!</span>
                    </div>
                  </div>
                )}
              </div>
            </TutorialStep>
          </div>

          {/* Complete Button */}
          {completedSteps.length === 3 && (
            <div className="mt-12 text-center animate-fadeIn">
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-8 mb-6 border border-purple-200">
                <div className="text-6xl mb-4">🎉</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  모든 준비가 완료되었습니다!
                </h2>
                <p className="text-gray-600">
                  이제 대시보드에서 본격적으로 시작해보세요
                </p>
              </div>
              <button
                onClick={handleFinishTutorial}
                className="px-12 py-4 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-lg font-semibold rounded-xl hover:shadow-2xl hover:scale-105 transition-all"
              >
                대시보드로 이동
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
