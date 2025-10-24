import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface ImageUploadProps {
  onUploadSuccess: (imageUrl: string, imageId: number) => void;
  onUploadError?: (error: string) => void;
  projectId?: number;
  maxSize?: number; // in MB
}

export default function ImageUpload({
  onUploadSuccess,
  onUploadError,
  projectId,
  maxSize = 10,
}: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    async (acceptedFiles: File[], rejectedFiles: any[]) => {
      setError(null);

      // Handle rejected files
      if (rejectedFiles.length > 0) {
        const rejection = rejectedFiles[0];
        if (rejection.errors[0]?.code === 'file-too-large') {
          setError(`파일 크기는 ${maxSize}MB 이하여야 합니다`);
        } else if (rejection.errors[0]?.code === 'file-invalid-type') {
          setError('PNG, JPG, JPEG 파일만 업로드 가능합니다');
        } else {
          setError('파일 업로드에 실패했습니다');
        }
        onUploadError?.(rejection.errors[0]?.message || '파일 업로드 실패');
        return;
      }

      const file = acceptedFiles[0];
      if (!file) return;

      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);

      // Upload to server
      setIsUploading(true);
      setUploadProgress(0);

      try {
        const formData = new FormData();
        formData.append('file', file);
        if (projectId) {
          formData.append('project_id', projectId.toString());
        }

        // Simulate progress (replace with actual progress tracking)
        const progressInterval = setInterval(() => {
          setUploadProgress((prev) => Math.min(prev + 10, 90));
        }, 200);

        const response = await fetch('/api/v1/images/upload', {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });

        clearInterval(progressInterval);
        setUploadProgress(100);

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || '업로드 실패');
        }

        const data = await response.json();
        onUploadSuccess(data.original_url, data.image_id);
      } catch (err: any) {
        setError(err.message || '업로드 중 오류가 발생했습니다');
        onUploadError?.(err.message);
        setPreview(null);
      } finally {
        setIsUploading(false);
        setUploadProgress(0);
      }
    },
    [maxSize, projectId, onUploadSuccess, onUploadError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
    },
    maxFiles: 1,
    maxSize: maxSize * 1024 * 1024,
    disabled: isUploading,
  });

  const handleRemove = () => {
    setPreview(null);
    setError(null);
  };

  return (
    <div className="w-full">
      {!preview ? (
        <div
          {...getRootProps()}
          className={`relative border-4 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
            isDragActive
              ? 'border-purple-500 bg-purple-50'
              : error
              ? 'border-red-300 bg-red-50'
              : 'border-gray-300 hover:border-purple-400 hover:bg-gray-50'
          } ${isUploading ? 'pointer-events-none opacity-50' : ''}`}
        >
          <input {...getInputProps()} />

          <div className="flex flex-col items-center">
            {/* Icon */}
            <div
              className={`w-20 h-20 rounded-full flex items-center justify-center mb-6 ${
                error
                  ? 'bg-red-100'
                  : 'bg-gradient-to-br from-purple-100 to-blue-100'
              }`}
            >
              {error ? (
                <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              )}
            </div>

            {/* Text */}
            <h3 className="text-xl font-bold mb-2 text-gray-900">
              {isDragActive
                ? '여기에 놓으세요'
                : error
                ? '다시 시도해주세요'
                : '이미지를 드래그하거나 클릭하세요'}
            </h3>
            <p className="text-gray-600 mb-4">
              PNG, JPG 파일 지원 (최대 {maxSize}MB)
            </p>

            {/* Error Message */}
            {error && (
              <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-2 rounded-lg text-sm mb-4">
                {error}
              </div>
            )}

            {/* Button */}
            {!error && (
              <button className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-xl hover:shadow-lg transition-all">
                파일 선택
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="relative rounded-2xl overflow-hidden shadow-xl">
          {/* Preview Image */}
          <div className="relative bg-gray-100">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-auto max-h-96 object-contain"
            />

            {/* Upload Progress Overlay */}
            {isUploading && (
              <div className="absolute inset-0 bg-black/50 flex flex-col items-center justify-center">
                <div className="w-24 h-24 relative mb-4">
                  <svg className="w-24 h-24 transform -rotate-90">
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="white"
                      strokeOpacity="0.3"
                      strokeWidth="8"
                      fill="none"
                    />
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="white"
                      strokeWidth="8"
                      fill="none"
                      strokeDasharray={`${2 * Math.PI * 40}`}
                      strokeDashoffset={`${2 * Math.PI * 40 * (1 - uploadProgress / 100)}`}
                      className="transition-all duration-300"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-white font-bold text-xl">{uploadProgress}%</span>
                  </div>
                </div>
                <p className="text-white font-medium">업로드 중...</p>
              </div>
            )}
          </div>

          {/* Actions */}
          {!isUploading && (
            <div className="absolute top-4 right-4 flex gap-2">
              <button
                onClick={handleRemove}
                className="p-2 bg-white/90 backdrop-blur-sm rounded-lg hover:bg-white shadow-lg transition-all"
                title="제거"
              >
                <svg className="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}

          {/* File Info */}
          {!isUploading && (
            <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-lg shadow-lg">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm font-medium text-gray-700">업로드 완료</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Upload Tips */}
      {!preview && !error && (
        <div className="mt-4 p-4 bg-blue-50 rounded-xl border border-blue-200">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="text-sm text-blue-800">
              <p className="font-semibold mb-1">최상의 결과를 위한 팁:</p>
              <ul className="space-y-1 text-blue-700">
                <li>• 배경이 단순한 이미지가 좋습니다</li>
                <li>• 상품이 중앙에 위치하면 더 좋습니다</li>
                <li>• 고해상도 이미지를 사용하세요</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
