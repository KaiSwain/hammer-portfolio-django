import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* TEMP DEBUG BANNER TO CONFIRM FRONTEND IS SERVING ROOT. REMOVE AFTER VERIFICATION. */}
      <div className="bg-red-600 text-white text-center py-2 text-sm font-semibold">FRONTEND SERVED ✔ If you see this, routing works. Remove banner in page.js.</div>
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Image
                src="/Hammer-Primary-Blue-Logo.png"
                alt="If I Had A Hammer Logo"
                width={120}
                height={40}
                className="h-10 w-auto"
                priority
              />
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/login"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Login
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Welcome to the{" "}
              <span className="text-blue-600">Hammer Portal</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Your comprehensive platform for workforce development, student management, 
              and training certification. Empowering the next generation of skilled tradespeople.
            </p>
            
            <div className="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
              <Link
                href="/login"
                className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Teacher Portal
              </Link>
              <Link
                href="/login"
                className="inline-block bg-gray-100 text-gray-900 px-8 py-3 rounded-lg text-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Access Your Account
              </Link>
            </div>
          </div>

          {/* Quick Access Cards */}
          <div className="grid md:grid-cols-2 gap-8 mb-12 max-w-4xl mx-auto">
            <Link
              href="/login"
              className="group bg-blue-600 hover:bg-blue-700 text-white rounded-xl p-8 transition-all duration-200 transform hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-4xl mb-4">👩‍🏫</div>
              <h3 className="text-2xl font-semibold mb-3">Teacher Portal</h3>
              <p className="text-blue-100">Access student portfolios, assessments, and progress tracking</p>
            </Link>

            <div className="bg-gray-100 rounded-xl p-8 border-2 border-dashed border-gray-300">
              <div className="text-4xl mb-4">👨‍🎓</div>
              <h3 className="text-2xl font-semibold mb-3 text-gray-600">Student Access</h3>
              <p className="text-gray-500">Coming Soon - Direct student portal access</p>
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 text-left max-w-5xl mx-auto">
            <div className="bg-orange-50 rounded-lg p-6 border border-orange-200">
              <div className="text-3xl mb-4">📊</div>
              <h4 className="font-semibold text-gray-800 mb-3 text-lg">Assessment Tracking</h4>
              <p className="text-gray-600">Comprehensive personality and safety assessments including DISC, 16 Types, Enneagram, and OSHA certifications</p>
            </div>

            <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
              <div className="text-3xl mb-4">📋</div>
              <h4 className="font-semibold text-gray-800 mb-3 text-lg">AI-Powered Summaries</h4>
              <p className="text-gray-600">Intelligent personality summaries and recommendations for employers and career development</p>
            </div>

            <div className="bg-green-50 rounded-lg p-6 border border-green-200">
              <div className="text-3xl mb-4">🏗️</div>
              <h4 className="font-semibold text-gray-800 mb-3 text-lg">Career Ready</h4>
              <p className="text-gray-600">Preparing students for successful careers in construction and skilled trades</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-500">
              Building careers, one student at a time.
            </p>
            <p className="text-gray-400 text-sm mt-2">
              © 2024 If I Had A Hammer. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
