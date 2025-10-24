interface TutorialStepProps {
  step: number;
  title: string;
  description: string;
  isActive: boolean;
  isCompleted: boolean;
  children: React.ReactNode;
}

export default function TutorialStep({
  step,
  title,
  description,
  isActive,
  isCompleted,
  children,
}: TutorialStepProps) {
  return (
    <div
      className={`transition-all duration-500 ${
        isActive ? 'opacity-100' : 'opacity-40 pointer-events-none'
      }`}
    >
      {/* Step Header */}
      <div className="flex items-center gap-4 mb-6">
        <div
          className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all ${
            isCompleted
              ? 'bg-green-500 text-white'
              : isActive
              ? 'bg-gradient-to-br from-purple-500 to-blue-500 text-white'
              : 'bg-gray-200 text-gray-500'
          }`}
        >
          {isCompleted ? (
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          ) : (
            step
          )}
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900">{title}</h3>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>

      {/* Step Content */}
      <div className={`ml-16 ${isActive ? 'animate-fadeIn' : ''}`}>
        {children}
      </div>
    </div>
  );
}
