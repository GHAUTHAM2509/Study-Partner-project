"use client";

import { useState, useEffect, useRef } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';

interface PaperQuestion {
  questions: string[];
}

export default function ChatPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const courseName = params.courseName as string;
  const paperId = searchParams.get('paperId');

  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: 'user' | 'bot'; content: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [paperQuestions, setPaperQuestions] = useState<string[] | null>(null);
  const [questionsLoading, setQuestionsLoading] = useState(true);

  const chatContainerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Effect to fetch paper questions if paperId exists
  useEffect(() => {
    if (paperId && courseName) {
      setQuestionsLoading(true);
      fetch(`http://localhost:8000/api/papers/${courseName}/${paperId}`)
        .then(res => res.json())
        .then((data: PaperQuestion) => {
          if (data.questions) {
            setPaperQuestions(data.questions);
          } else {
            setPaperQuestions(['Failed to load questions.']);
          }
        })
        .catch(() => setPaperQuestions(['Error fetching questions.']))
        .finally(() => setQuestionsLoading(false));
    } else {
      setQuestionsLoading(false);
    }
  }, [paperId, courseName]);

  // Effect to scroll to the bottom of the chat
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Auto-grow textarea height
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const handleSendMessage = async () => {
    if (!message.trim() || loading) return;

    const newHistory = [...chatHistory, { role: 'user' as const, content: message }];
    setChatHistory(newHistory);
    setMessage('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message, courseName }),
      });
      const data = await response.json();
      setChatHistory([...newHistory, { role: 'bot' as const, content: data.answer || 'Sorry, I encountered an error.' }]);
    } catch (error) {
      setChatHistory([...newHistory, { role: 'bot' as const, content: 'Failed to connect to the server.' }]);
    } finally {
      setLoading(false);
    }
  };

  const formatCourseName = (name: string) => {
    return name
      ? name.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
      : 'Chat';
  };

  return (
    <div className="flex h-screen bg-[#23272D] text-white font-open-sans">
      {/* Questions Side Panel */}
      {paperId && (
        <div className="w-[360px] bg-[#2C3138] p-4 flex flex-col" style={{ minWidth: 250, maxWidth: 400 }}>
          <h2 className="text-xl font-bold mb-4 border-b border-gray-500 pb-2">Paper Questions</h2>
          <div className="flex-grow overflow-y-auto">
            {questionsLoading ? (
              <p>Loading questions...</p>
            ) : (
              <ul className="space-y-3">
                {paperQuestions?.map((q, index) => (
                  <li key={index} className="text-sm text-gray-300 bg-[#40444A] p-2 rounded-md">
                    {q}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {/* Main Chat Window */}
      <div className="flex flex-col flex-1">
        <header className="flex items-center p-4 bg-[#2C3138] border-b border-gray-700">
          <Link href={`/courses/${courseName}`}>
              <Image src="/images/logo.svg" alt="Logo" width={50} height={50} />
          </Link>
          <h1 className="text-3xl font-bold ml-4">{formatCourseName(courseName)}</h1>
        </header>

        <main ref={chatContainerRef} className="flex-grow p-6 px-20 overflow-y-auto">
          <div className="space-y-4">
            {chatHistory.map((chat, index) => (
              <div key={index} className={`flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={
                    chat.role === 'user'
                      ? 'max-w-lg p-3 rounded-lg bg-[#40444A] full-length break-words whitespace-pre-wrap'
                      : 'w-full p-3 rounded-lg bg-[#23272D] break-words whitespace-pre-wrap'
                  }
                >
                  {chat.role === 'bot'
                    ? <ReactMarkdown>{chat.content}</ReactMarkdown>
                    : chat.content
                  }
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="w-full p-3 rounded-lg bg-[#23272D] break-words whitespace-pre-wrap">
                  Thinking...
                </div>
              </div>
            )}
          </div>
        </main>

        <footer className="p-4 px-20 bg-[#23272D]  border-gray-700">
          <div className="flex items-center bg-[#40444A] rounded-lg p-2">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Ask your question..."
              className="flex-grow bg-transparent focus:outline-none px-2 resize-none min-h-[40px] max-h-40"
              disabled={loading}
              rows={1}
            />
            <button onClick={handleSendMessage} disabled={loading} className="bg-blue-600 hover:bg-blue-700 rounded-md p-2 ml-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}

