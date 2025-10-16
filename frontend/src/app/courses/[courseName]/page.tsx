"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';

interface File {
  name: string;
  type: 'pdf' | 'ppt';
}

// Updated Paper interface to match your data structure
interface Paper {
  title: string;
  link: string;
  pdf_link: string;
  course_code: string;
  tags: string[];
}

export default function CoursePage() {
  const params = useParams();
  const courseName = params.courseName as string;
  const [files, setFiles] = useState<File[]>([]);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'files' | 'papers'>('files');

  useEffect(() => {
    if (!courseName) return;

    setLoading(true);
    let url = '';
    if (activeTab === 'files') {
      url = `http://localhost:8000/api/files/${courseName}`;
    } else {
      url = `http://localhost:8000/api/papers/${courseName}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (activeTab === 'files') {
          if (data.files) {
            setFiles(data.files);
          } else {
            console.error("API did not return files:", data.error);
            setFiles([]);
          }
        } else {
          if (data.papers) {
            setPapers(data.papers);
          } else {
            console.error("API did not return papers:", data.error);
            setPapers([]);
          }
        }
      })
      .finally(() => {
        setLoading(false);
      });
  }, [courseName, activeTab]);

  const getFileIcon = (type: string) => {
    if (type === 'pdf') {
      return '/images/pdf-icon.svg';
    }
    return '/images/ppt-icon.svg';
  };

  const formatCourseName = (name: string) => {
    return name
      .split('-')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // SVG Icon for View
  const ViewIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
    </svg>
  );

  // SVG Icon for Download
  const DownloadIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
  );

  return (
    <div className="bg-[#23272D] text-white min-h-screen p-8 font-open-sans">
      <header className="flex items-center mb-16">
        <Link href="/">
            <Image src="/images/logo.svg" alt="Study Partner Logo" width={60} height={60} />
        </Link>
        <h1 className="text-4xl font-bold ml-4">{formatCourseName(courseName)}</h1>
      </header>
      <main className="px-16 py-0">
        <div className="flex gap-8 mb-8 border-b border-gray-600">
          <button
            onClick={() => setActiveTab('files')}
            className={`text-2xl font-semibold pb-2 ${activeTab === 'files' ? 'text-white border-b-2 border-white' : 'text-gray-400'}`}
          >
            Files
          </button>
          <button
            onClick={() => setActiveTab('papers')}
            className={`text-2xl font-semibold pb-2 ${activeTab === 'papers' ? 'text-white border-b-2 border-white' : 'text-gray-400'}`}
          >
            Papers
          </button>
        </div>
        <div className="border border-gray-600 rounded-lg p-4 h-96 overflow-y-auto">
          {loading ? (
            <div className="flex justify-center items-center h-full"><p>Loading...</p></div>
          ) : activeTab === 'files' ? (
            <div className="flex flex-col gap-2">
              {files.length > 0 ? files.map((file) => (
                <div key={file.name} className="bg-[#2C3138] rounded-lg p-4 flex items-center justify-between hover:bg-[#40444A] transition-colors">
                  <div className="flex items-center">
                    <Image src={getFileIcon(file.type)} alt={`${file.type} icon`} width={40} height={40} />
                    <span className="ml-4">{file.name}</span>
                  </div>
                  <div className="flex gap-2">
                    <a href={`http://localhost:8000/api/files/${courseName}/${file.name}`} target="_blank" rel="noopener noreferrer" className="flex items-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded transition-colors text-sm">
                      <ViewIcon /> View
                    </a>
                    <a href={`http://localhost:8000/api/files/${courseName}/${file.name}`} download className="flex items-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-3 rounded transition-colors text-sm">
                      <DownloadIcon /> Download
                    </a>
                  </div>
                </div>
              )) : <p className="text-center">No files found for this course.</p>}
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {papers.length > 0 ? papers.map((paper) => (
                <div key={paper.link} className="bg-[#2C3138] rounded-lg p-4 flex flex-col sm:flex-row justify-between hover:bg-[#40444A] transition-colors">
                  <div className="flex-grow mb-3 sm:mb-0">
                    <h3 className="font-semibold text-lg">{paper.title} <span className="text-sm text-gray-400 font-mono">({paper.course_code})</span></h3>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {paper.tags.map(tag => (
                        <span key={tag} className="bg-gray-600 text-gray-200 text-xs font-semibold px-2.5 py-0.5 rounded-full">{tag}</span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-2 items-center flex-shrink-0">
                    <a href={paper.link} target="_blank" rel="noopener noreferrer" className="flex items-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded transition-colors text-sm">
                      <ViewIcon /> View
                    </a>
                    <a href={paper.pdf_link} download target="_blank" rel="noopener noreferrer" className="flex items-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-3 rounded transition-colors text-sm">
                      <DownloadIcon /> Download
                    </a>
                  </div>
                </div>
              )) : <p className="text-center">No papers found for this course.</p>}
            </div>
          )}
        </div>
      </main>
      <div className="flex justify-center items-center mt-16">
        <Link href={`/chat/${courseName}`}>
          <button className="bg-[#ffffff] hover:bg-[#D9D9D9] text-2xl text-[#23272D] font-bold py-4 px-8 rounded-lg transition-colors font-open-sans">
            Try Student-Partner AI
          </button>
        </Link>
      </div>
    </div>
  );
}
