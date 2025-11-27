import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import html2pdf from 'html2pdf.js'

function App() {
    const [message, setMessage] = useState('Loading...')
    const [transcript, setTranscript] = useState(null)
    const [summary, setSummary] = useState(null)
    const [loadingSummary, setLoadingSummary] = useState(false)
    const [videoId, setVideoId] = useState('')

    useEffect(() => {
        fetch('/api/')
            .then(res => res.json())
            .then(data => setMessage(data.message))
            .catch(err => setMessage('Error connecting to backend'))
    }, [])

    const fetchTranscript = async () => {
        console.log(`Fetching transcript for videoId: ${videoId}`);
        setTranscript(null);
        setSummary(null);
        try {
            // Encode videoId to handle special characters in URLs
            const encodedVideoId = encodeURIComponent(videoId);
            const res = await fetch(`/api/api/transcript?video_id=${encodedVideoId}`)
            console.log(`Response status: ${res.status}`);
            const data = await res.json()
            console.log('Received data:', data);

            if (res.ok) {
                if (Array.isArray(data.transcript)) {
                    setTranscript(data.transcript)
                } else {
                    console.error('Transcript is not an array:', data.transcript);
                    alert('Received invalid transcript format from backend.');
                }
            } else {
                console.error('Backend error:', data);
                alert(`Backend Error: ${data.detail}`)
            }
        } catch (error) {
            console.error('Fetch error:', error)
            alert(`Failed to fetch transcript: ${error.message}`)
        }
    }

    const fetchSummary = async () => {
        if (!videoId) return;
        setLoadingSummary(true);
        try {
            const encodedVideoId = encodeURIComponent(videoId);
            const res = await fetch(`/api/api/summarize?video_id=${encodedVideoId}`)
            const data = await res.json()

            if (res.ok) {
                setSummary(data.summary)
            } else {
                alert(`Error fetching summary: ${data.detail}`)
            }
        } catch (error) {
            console.error('Summary fetch error:', error)
            alert(`Failed to fetch summary: ${error.message}`)
        } finally {
            setLoadingSummary(false);
        }
    }

    const copyToClipboard = () => {
        if (summary) {
            navigator.clipboard.writeText(summary);
            alert('Notes copied to clipboard!');
        }
    }

    const handleDownloadPDF = () => {
        const element = document.getElementById('summary-content');
        const opt = {
            margin: 10,
            filename: 'TubeNotes.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        html2pdf().from(element).save();
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4 font-sans">
            <h1 className="text-5xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">TubeNotes</h1>
            <p className="mb-8 text-lg text-gray-400">Backend Status: <span className={`font-semibold ${message.includes('running') ? 'text-green-400' : 'text-red-400'}`}>{message}</span></p>

            <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-lg border border-gray-700">
                <input
                    type="text"
                    placeholder="Enter YouTube Video ID"
                    className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg mb-6 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                    value={videoId}
                    onChange={(e) => setVideoId(e.target.value)}
                />
                <div className="flex gap-4">
                    <button
                        onClick={fetchTranscript}
                        className="flex-1 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition font-semibold shadow-lg"
                    >
                        Get Transcript
                    </button>
                    <button
                        onClick={fetchSummary}
                        disabled={loadingSummary || !videoId}
                        className={`flex-1 p-3 rounded-lg transition font-semibold shadow-lg ${loadingSummary || !videoId ? 'bg-gray-600 cursor-not-allowed text-gray-400' : 'bg-purple-600 hover:bg-purple-700 text-white'}`}
                    >
                        {loadingSummary ? 'Summarizing...' : 'Get Summary'}
                    </button>
                </div>
            </div>

            <div className="flex flex-col md:flex-row gap-8 w-full max-w-6xl mt-12">
                {transcript && Array.isArray(transcript) && (
                    <div className="flex-1 bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 h-96 overflow-y-auto custom-scrollbar">
                        <h2 className="text-2xl font-bold mb-4 text-blue-400 sticky top-0 bg-gray-800 pb-2 border-b border-gray-700">Transcript</h2>
                        <ul className="space-y-3">
                            {transcript.map((item, index) => (
                                <li key={index} className="text-gray-300 leading-relaxed">
                                    <span className="font-mono text-sm text-gray-500 mr-2">{Math.floor(item.start)}s:</span> {item.text}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {summary && (
                    <div className="flex-1 bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 h-[32rem] overflow-y-auto custom-scrollbar relative">
                        <div className="flex justify-between items-center mb-4 sticky top-0 bg-gray-800 pb-2 border-b border-gray-700 z-10">
                            <h2 className="text-2xl font-bold text-purple-400">AI Notes</h2>
                            <div className="flex gap-2">
                                <button
                                    onClick={copyToClipboard}
                                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm transition border border-gray-600"
                                >
                                    Copy
                                </button>
                                <button
                                    onClick={handleDownloadPDF}
                                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 rounded text-sm transition shadow-md"
                                >
                                    Download PDF
                                </button>
                            </div>
                        </div>
                        <div id="summary-content" className="prose prose-invert prose-blue max-w-none p-4 bg-gray-800">
                            <ReactMarkdown>{summary}</ReactMarkdown>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default App
