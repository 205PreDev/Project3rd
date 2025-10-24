import { useState, useEffect } from 'react';

interface ChecklistItem {
  id: string;
  title: string;
  description: string;
  reward: number;
  completed: boolean;
}

export default function Checklist() {
  const [items, setItems] = useState<ChecklistItem[]>([
    {
      id: 'create_project',
      title: '첫 프로젝트 생성',
      description: '프로젝트를 만들어보세요',
      reward: 2,
      completed: false,
    },
    {
      id: 'upload_image',
      title: '이미지 업로드',
      description: '상품 이미지를 업로드해보세요',
      reward: 2,
      completed: false,
    },
    {
      id: 'generate_background',
      title: '배경 생성',
      description: 'AI로 배경을 생성해보세요',
      reward: 2,
      completed: false,
    },
    {
      id: 'generate_caption',
      title: '광고 문구 생성',
      description: 'AI 광고 문구를 생성해보세요',
      reward: 2,
      completed: false,
    },
    {
      id: 'share_sns',
      title: 'SNS 공유',
      description: '완성된 이미지를 SNS에 공유해보세요',
      reward: 2,
      completed: false,
    },
  ]);

  const [totalReward, setTotalReward] = useState(0);
  const [showRewardModal, setShowRewardModal] = useState(false);

  const completedCount = items.filter((item) => item.completed).length;
  const progress = (completedCount / items.length) * 100;

  const handleCompleteItem = (id: string) => {
    setItems((prev) =>
      prev.map((item) => {
        if (item.id === id && !item.completed) {
          setTotalReward((r) => r + item.reward);
          setShowRewardModal(true);
          setTimeout(() => setShowRewardModal(false), 3000);
          return { ...item, completed: true };
        }
        return item;
      })
    );
  };

  // 테스트용 자동 완료 (실제로는 API 연동)
  useEffect(() => {
    const timer = setTimeout(() => {
      handleCompleteItem('create_project');
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">시작 가이드</h2>
          <div className="flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-bold text-purple-700">{totalReward} 크레딧 획득!</span>
          </div>
        </div>
        <p className="text-gray-600">
          체크리스트를 완료하고 크레딧을 받으세요
        </p>

        {/* Progress Bar */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>
              {completedCount} / {items.length} 완료
            </span>
            <span className="font-semibold">{Math.round(progress)}%</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-500"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Checklist Items */}
      <div className="space-y-3">
        {items.map((item, index) => (
          <div
            key={item.id}
            className={`flex items-start gap-4 p-4 rounded-xl transition-all ${
              item.completed
                ? 'bg-green-50 border border-green-200'
                : 'bg-gray-50 hover:bg-gray-100 border border-transparent'
            }`}
          >
            {/* Checkbox */}
            <div className="flex-shrink-0">
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center transition-all ${
                  item.completed
                    ? 'bg-green-500'
                    : 'bg-white border-2 border-gray-300'
                }`}
              >
                {item.completed && (
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            </div>

            {/* Content */}
            <div className="flex-1">
              <h3
                className={`font-semibold ${
                  item.completed ? 'text-green-700 line-through' : 'text-gray-900'
                }`}
              >
                {item.title}
              </h3>
              <p className="text-sm text-gray-600">{item.description}</p>
            </div>

            {/* Reward Badge */}
            <div
              className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold ${
                item.completed
                  ? 'bg-green-200 text-green-700'
                  : 'bg-purple-100 text-purple-700'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              +{item.reward}
            </div>
          </div>
        ))}
      </div>

      {/* Completion Message */}
      {completedCount === items.length && (
        <div className="mt-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 text-center border border-purple-200 animate-fadeIn">
          <div className="text-4xl mb-2">🎉</div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">
            모든 체크리스트 완료!
          </h3>
          <p className="text-gray-600">
            총 {totalReward} 크레딧을 획득하셨습니다
          </p>
        </div>
      )}

      {/* Reward Notification */}
      {showRewardModal && (
        <div className="fixed top-4 right-4 z-50 animate-slideIn">
          <div className="bg-white rounded-xl shadow-2xl p-6 border-2 border-purple-200 max-w-sm">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-900">크레딧 획득!</h4>
                <p className="text-sm text-gray-600">
                  2 크레딧이 추가되었습니다
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
