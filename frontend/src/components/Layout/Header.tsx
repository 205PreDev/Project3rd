import { useNavigate } from 'react-router-dom';

interface HeaderProps {
  user?: {
    email: string;
    credits: number;
  };
  showCredits?: boolean;
  onLogout?: () => void;
}

export default function Header({ user, showCredits = true, onLogout }: HeaderProps) {
  const navigate = useNavigate();

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <button
            onClick={() => navigate(user ? '/dashboard' : '/')}
            className="flex items-center space-x-2 hover:opacity-80 transition"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg"></div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              AI 이미지 생성
            </span>
          </button>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            {user ? (
              <>
                {/* Credits */}
                {showCredits && (
                  <div className="flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full">
                    <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="font-bold text-purple-700">{user.credits} 크레딧</span>
                  </div>
                )}

                {/* User Menu */}
                <div className="relative group">
                  <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-all">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {user.email[0]?.toUpperCase() || 'U'}
                    </div>
                    <span className="text-sm font-medium text-gray-700 hidden md:block">{user.email}</span>
                  </button>

                  {/* Dropdown */}
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                    <div className="p-2 space-y-1">
                      <button
                        onClick={() => navigate('/dashboard')}
                        className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 rounded-lg transition-all"
                      >
                        대시보드
                      </button>
                      <button
                        onClick={onLogout}
                        className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 rounded-lg transition-all"
                      >
                        로그아웃
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <>
                <button
                  onClick={() => navigate('/trial')}
                  className="px-4 py-2 text-gray-700 font-medium hover:text-gray-900 transition"
                >
                  무료 체험
                </button>
                <button
                  onClick={() => navigate('/signup')}
                  className="px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
                >
                  시작하기
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
