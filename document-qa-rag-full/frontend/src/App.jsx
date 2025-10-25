import React, { useState } from 'react'
import axios from 'axios'

export default function App() {
  const [apiBase, setApiBase] = useState('http://localhost:8000/api')
  const [file, setFile] = useState(null)
  const [uploadRes, setUploadRes] = useState(null)
  const [sessionId, setSessionId] = useState('demo_session')
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)

  const handleUpload = async () => {
    if (!file) return alert('Please choose a file first!')
    setUploading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const res = await axios.post(`${apiBase}/upload`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setUploadRes(res.data)
    } catch (err) {
      alert('Upload failed: ' + err.message)
    } finally {
      setUploading(false)
    }
  }

  const handleAsk = async () => {
    if (!query.trim()) return alert('Please enter a question!')
    setLoading(true)
    try {
      const res = await axios.post(`${apiBase}/qa`, {
        session_id: sessionId,
        query,
      })
      setAnswer(res.data.answer)
    } catch (err) {
      alert('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 flex flex-col items-center py-10 font-sans">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-[700px]">
        <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
          📄 Document Q&A — RAG Demo
        </h2>

        {/* API Base */}
        <div className="mb-4">
          <label className="font-semibold text-gray-700">API Base URL:</label>
          <input
            value={apiBase}
            onChange={(e) => setApiBase(e.target.value)}
            className="w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-purple-400 outline-none"
          />
        </div>

        {/* Upload Section */}
        <div className="bg-gradient-to-r from-purple-200 to-pink-200 rounded-xl p-4 mb-6 shadow-inner">
          <h3 className="font-semibold text-lg mb-2">1️⃣ Upload your document</h3>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="block mb-3"
          />
          {file && (
            <p className="text-sm text-gray-700 mb-3">
              Selected: <strong>{file.name}</strong> ({(file.size / 1024).toFixed(1)} KB)
            </p>
          )}
          <button
            onClick={handleUpload}
            disabled={uploading}
            className={`px-5 py-2 rounded-lg text-white font-medium transition ${
              uploading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105 shadow-lg'
            }`}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>

          {uploadRes && (
            <pre className="bg-white text-sm mt-3 p-2 rounded-md border border-gray-200 overflow-x-auto">
              {JSON.stringify(uploadRes, null, 2)}
            </pre>
          )}
        </div>

        {/* Ask Section */}
        <div className="bg-gradient-to-r from-blue-200 to-cyan-200 rounded-xl p-4 shadow-inner">
          <h3 className="font-semibold text-lg mb-2">2️⃣ Ask your question</h3>

          <label className="font-medium text-gray-700">Session ID:</label>
          <input
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="border border-gray-300 rounded-lg p-2 ml-2 w-1/2 focus:ring-2 focus:ring-blue-400 outline-none"
          />
          <textarea
            rows={4}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your question here..."
            className="w-full border border-gray-300 rounded-lg p-3 mt-3 focus:ring-2 focus:ring-blue-400 outline-none"
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className={`mt-3 px-5 py-2 rounded-lg text-white font-medium transition ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-500 to-purple-500 hover:scale-105 shadow-lg'
            }`}
          >
            {loading ? 'Thinking...' : 'Ask'}
          </button>

          {answer && (
            <div className="bg-white rounded-lg p-4 mt-4 border-l-4 border-blue-400 shadow">
              <strong className="text-blue-600 text-lg">Answer:</strong>
              <p className="mt-2 text-gray-800 whitespace-pre-wrap">{answer}</p>
            </div>
          )}
        </div>
      </div>

      <footer className="mt-6 text-sm text-gray-600">
        💡 Built with ❤️ using React & Tailwind
      </footer>
    </div>
  )
}
