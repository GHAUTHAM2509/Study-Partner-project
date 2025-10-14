"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';

interface File {
  name: string;
  type: 'pdf' | 'ppt';
}

export default function CoursePage() {
  const params = useParams();
  const courseName = params.courseName as string;
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (courseName) {
      fetch(`http://localhost:8000/api/files/${courseName}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.files) {
            setFiles(data.files);
          } else {
            console.error("API did not return files:", data.error);
          }
          setLoading(false);
        });
    }
  }, [courseName]);

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

  return (
    <div className="bg-[#23272D] text-white min-h-screen p-8 font-open-sans">
      <header className="flex items-center mb-16">
        <Link href="/">
            <Image src="/images/logo.svg" alt="Study Partner Logo" width={60} height={60} />
        </Link>
        <h1 className="text-4xl font-bold ml-4">{formatCourseName(courseName)}</h1>
      </header>
      <main className="px-16 py-0">
        <h2 className="text-3xl font-semibold mb-12 ">Files</h2>
        <div className="border border-gray-600 rounded-lg p-4 h-96 overflow-y-auto">
          {loading ? (
            <p>Loading files...</p>
          ) : (
            <div className="flex flex-col">
              {files.map((file) => (
                <a
                  key={file.name}
                  href={`http://localhost:8000/api/files/${courseName}/${file.name}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-[#23272D] rounded-lg p-4 flex items-center hover:bg-[#40444A] transition-colors"
                >
                  <Image src={getFileIcon(file.type)} alt={`${file.type} icon`} width={40} height={40} />
                  <span className="ml-4">{file.name}</span>
                </a>
              ))}
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
