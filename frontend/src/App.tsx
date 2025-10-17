import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI 이커머스 이미지 생성기
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          상품 이미지와 광고 문구를 자동으로 생성하세요
        </p>
        <button
          onClick={() => setCount((count) => count + 1)}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          클릭 횟수: {count}
        </button>
      </div>
    </div>
  )
}

export default App
