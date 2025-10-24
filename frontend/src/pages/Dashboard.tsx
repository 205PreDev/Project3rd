import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ImageUpload from '../components/ImageUpload';
import StyleSelector from '../components/StyleSelector';
import CaptionGenerator from '../components/CaptionGenerator';
import ShareModal from '../components/ShareModal';

interface Project {
  id: number;
  name: string;
  image_count: number;
  created_at: string;
}

interface Image {
  id: number;
  project_id: number;
  original_url: string;
  processed_url?: string;
  caption?: string;
  created_at: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [images, setImages] = useState<Image[]>([]);
  const [selectedImage, setSelectedImage] = useState<Image | null>(null);

  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'upload' | 'style' | 'caption'>('upload');

  useEffect(() => {
    fetchUser();
    fetchProjects();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      fetchImages(selectedProject.id);
    }
  }, [selectedProject]);

  const fetchUser = async () => {
    try {
      const response = await fetch('/api/v1/auth/me', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      }
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/v1/projects', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setProjects(data);
        if (data.length > 0) {
          setSelectedProject(data[0]);
        }
      }
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    }
  };

  const fetchImages = async (projectId: number) => {
    try {
      const response = await fetch(`/api/v1/projects/${projectId}/images`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setImages(data);
      }
    } catch (error) {
      console.error('Failed to fetch images:', error);
    }
  };

  const handleLogout = () => {
    // Clear session and redirect
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg"></div>
              <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                AI 이미지 생성
              </span>
            </div>

            {/* User Info */}
            <div className="flex items-center gap-4">
              {/* Credits */}
              <div className="flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-bold text-purple-700">{user?.credits || 0} 크레딧</span>
              </div>

              {/* User Menu */}
              <div className="relative group">
                <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-all">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                    {user?.email?.[0]?.toUpperCase() || 'U'}
                  </div>
                  <span className="text-sm font-medium text-gray-700">{user?.email}</span>
                </button>

                {/* Dropdown */}
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-3 text-left text-gray-700 hover:bg-gray-50 rounded-xl transition-all"
                  >
                    로그아웃
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar - Projects */}
          <div className="col-span-3 space-y-4">
            <div className="bg-white rounded-2xl shadow-lg p-4">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-gray-900">프로젝트</h2>
                <button
                  onClick={() => setShowNewProjectModal(true)}
                  className="p-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>

              <div className="space-y-2">
                {projects.map((project) => (
                  <button
                    key={project.id}
                    onClick={() => setSelectedProject(project)}
                    className={`w-full p-3 rounded-xl text-left transition-all ${
                      selectedProject?.id === project.id
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg'
                        : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="font-semibold truncate">{project.name}</div>
                    <div className="text-xs opacity-80">{project.image_count || 0} 이미지</div>
                  </button>
                ))}

                {projects.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <p className="text-sm">프로젝트가 없습니다</p>
                    <p className="text-xs mt-1">+ 버튼으로 생성하세요</p>
                  </div>
                )}
              </div>
            </div>

            {/* Checklist Component */}
            <div className="bg-white rounded-2xl shadow-lg p-4">
              <h3 className="font-bold text-gray-900 mb-3">시작 가이드</h3>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-green-600">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>첫 프로젝트 생성</span>
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <div className="w-4 h-4 border-2 border-gray-300 rounded"></div>
                  <span>이미지 업로드</span>
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <div className="w-4 h-4 border-2 border-gray-300 rounded"></div>
                  <span>배경 생성</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Area */}
          <div className="col-span-9 space-y-6">
            {/* Tabs */}
            <div className="flex gap-2 bg-white rounded-2xl shadow-lg p-2">
              {[
                { id: 'upload', name: '이미지 업로드', icon: '📤' },
                { id: 'style', name: '배경 선택', icon: '🎨' },
                { id: 'caption', name: '광고 문구', icon: '✍️' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              {activeTab === 'upload' && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">이미지 업로드</h2>
                  <ImageUpload
                    onUploadSuccess={(url, id) => {
                      console.log('Uploaded:', url, id);
                      if (selectedProject) {
                        fetchImages(selectedProject.id);
                      }
                      setActiveTab('style');
                    }}
                    projectId={selectedProject?.id}
                  />
                </div>
              )}

              {activeTab === 'style' && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">배경 스타일 선택</h2>
                  <StyleSelector
                    onSelectStyle={(styleId) => {
                      console.log('Selected style:', styleId);
                      setActiveTab('caption');
                    }}
                  />
                </div>
              )}

              {activeTab === 'caption' && (
                <div>
                  <CaptionGenerator
                    imageId={selectedImage?.id || 1}
                    productDescription="상품 설명"
                    onCaptionGenerated={(caption) => {
                      console.log('Generated caption:', caption);
                    }}
                  />
                </div>
              )}
            </div>

            {/* Image Gallery */}
            {images.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">생성된 이미지</h2>
                  <button
                    onClick={() => setShowShareModal(true)}
                    className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-xl hover:shadow-lg transition-all"
                  >
                    공유하기
                  </button>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  {images.map((image) => (
                    <div
                      key={image.id}
                      className="relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all cursor-pointer group"
                      onClick={() => setSelectedImage(image)}
                    >
                      <img
                        src={image.processed_url || image.original_url}
                        alt="Generated"
                        className="w-full aspect-square object-cover"
                      />
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedImage(image);
                            setShowShareModal(true);
                          }}
                          className="px-4 py-2 bg-white text-gray-900 font-semibold rounded-lg hover:bg-gray-100 transition-all"
                        >
                          공유
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Share Modal */}
      {showShareModal && selectedImage && (
        <ShareModal
          isOpen={showShareModal}
          onClose={() => setShowShareModal(false)}
          imageUrl={selectedImage.processed_url || selectedImage.original_url}
          caption={selectedImage.caption}
          imageId={selectedImage.id}
        />
      )}
    </div>
  );
}
