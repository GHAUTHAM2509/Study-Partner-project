import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-[#23272D] text-white min-h-screen p-8 font-open-sans">
      <header className="flex items-center mb-16">
        <Image src="/images/logo.svg" alt="Study Partner Logo" width={60} height={60} />
        <h1 className="text-4xl font-bold ml-4">Study Partner</h1>
      </header>
      <main className="p-16">
        <h2 className="text-3xl font-semibold mb-12 ">Courses</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-16">
          <Link href="/courses/database-systems">
            <div
              className="bg-cover bg-center rounded-2xl p-12 flex items-end justify-start h-60 cursor-pointer hover:opacity-90 transition-opacity shadow-lg"
              style={{ backgroundImage: "url('/images/database.png')" }}>            
              <h3 className="text-2xl font-semibold text-left text-white">Database Systems</h3>
            </div>
          </Link>
          <Link href="/courses/operating-systems">
            <div className="bg-cover bg-center rounded-2xl p-12 flex items-end justify-start h-60 cursor-pointer hover:opacity-90 transition-opacity shadow-lg" style={{ backgroundImage: "url('/images/operating-systems.png')" }}>
              <h3 className="text-2xl font-semibold text-left text-white">Operating Systems</h3>
            </div>
          </Link>
          <Link href="/courses/cloud-computing">
            <div className="bg-cover bg-center rounded-2xl p-12 flex items-end justify-start h-60 cursor-pointer hover:opacity-90 transition-opacity shadow-lg" style={{ backgroundImage: "url('/images/cloud-computing.png')" }}>
              <h3 className="text-2xl font-semibold text-left text-white">Cloud Computing</h3>
            </div>
          </Link>
        </div>
      </main>
    </div>
  );
}