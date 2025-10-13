"use client";

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface Message {
  text: string;
  sender: 'user' | 'ai';
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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
        body: JSON.stringify({ question: input }),
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
    <div className="bg-[#23272D] text-white min-h-screen flex flex-col p-4 font-open-sans">
      <header className="flex items-center mb-4 p-4">
        <Link href="/">
          <Image src="/images/logo.svg" alt="Study Partner Logo" width={50} height={50} />
        </Link>
        <h1 className="text-3xl font-bold ml-4">Study Partner AI</h1>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-lg p-3 rounded-lg ${
                msg.sender === 'user' ? 'bg-blue-600' : 'bg-[#363A40]'
              }`}
            >
              <p style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-[#363A40] p-3 rounded-lg">
              <p>Thinking...</p>
            </div>
          </div>
        )}
      </main>

      <footer className="p-4">
        <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your notes..."
            className="flex-1 p-3 bg-[#363A40] rounded-lg focus:outline-none"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors disabled:opacity-50"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}
