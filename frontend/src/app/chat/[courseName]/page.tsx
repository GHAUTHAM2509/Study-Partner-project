"use client";

import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Message {
  text: string;
  sender: 'user' | 'ai';
}

export default function ChatPage() {
  const params = useParams();
  const courseName = params.courseName as string;
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Load messages from local storage on component mount
  useEffect(() => {
    if (courseName) {
      const savedMessages = localStorage.getItem(`chatHistory_${courseName}`);
      if (savedMessages) {
        setMessages(JSON.parse(savedMessages));
      }
    }
  }, [courseName]);

  // Save messages to local storage whenever they change
  useEffect(() => {
    if (courseName && messages.length > 0) {
      localStorage.setItem(`chatHistory_${courseName}`, JSON.stringify(messages));
    }
  }, [messages, courseName]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input, courseName: courseName }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const aiMessage: Message = { text: data.answer, sender: 'ai' };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Failed to get answer:', error);
      const errorMessage: Message = { text: 'Sorry, something went wrong. Please try again.', sender: 'ai' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-[#23272D] text-white h-screen flex flex-col font-open-sans">
      <header className="flex items-center mb-4 p-4 px-8 md:px-16">
        <Link href={`/courses/${courseName}`}>
          <Image src="/images/logo.svg" alt="Study Partner Logo" width={50} height={50} />
        </Link>
        <h1 className="text-3xl font-bold ml-4">Study Partner AI</h1>
      </header>

      <main className="flex-1 overflow-y-auto px-8 md:px-60 space-y-6">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`p-4 rounded-lg ${
                msg.sender === 'user'
                  ? 'bg-blue-600 max-w-2xl'
                  : 'bg-[#363A40] w-full'
              }`}
            >
              <p style={{ whiteSpace: 'pre-wrap' }} className="text-lg">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-[#363A40] p-4 rounded-lg w-full">
              <p className="text-lg">Thinking...</p>
            </div>
          </div>
        )}
      </main>

      <footer className="p-8 px-8 md:px-60">
        <form onSubmit={handleSendMessage} className="relative flex items-center">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage(e);
              }
            }}
            placeholder="Ask a question about your notes..."
            className="flex-1 p-3 pr-12 bg-[#363A40] rounded-lg focus:outline-none resize-none overflow-hidden text-lg"
            rows={1}
            style={{ maxHeight: '200px' }}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="absolute right-3 bottom-2.5 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full transition-colors disabled:opacity-50"
            disabled={isLoading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </form>
      </footer>
    </div>
  );
}
