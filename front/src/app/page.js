import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex items-center justify-center px-4">
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12 border border-gray-200">
          {/* Logo/Header */}
          <div className="mb-8">
            <div className="flex justify-center mb-4">
              <Image
                src="/Hammer-Primary-Blue-Logo.png"
                alt="If I Had A Hammer Logo"
                width={300}
                height={100}
                className="h-16 md:h-20 w-auto"
                priority
              />
            </div>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Empowering the next generation of skilled tradespeople through comprehensive 
              pre-apprenticeship training and assessment.
            </p>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Link
              href="/login"
              className="group bg-blue-600 hover:bg-blue-700 text-white rounded-xl p-6 transition-all duration-200 transform hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-2xl mb-2">👩‍🏫</div>
              <h3 className="text-xl font-semibold mb-2">Teacher Portal</h3>
              <p className="text-blue-100">Access student portfolios and assessments</p>
            </Link>

            <div className="bg-gray-100 rounded-xl p-6 border-2 border-dashed border-gray-300">
              <div className="text-2xl mb-2">👨‍🎓</div>
              <h3 className="text-xl font-semibold mb-2 text-gray-600">Student Access</h3>
              <p className="text-gray-500">Coming Soon - Direct student portal</p>
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 text-left">
            <div className="bg-orange-50 rounded-lg p-6 border border-orange-200">
              <div className="text-2xl mb-3">📊</div>
              <h4 className="font-semibold text-gray-800 mb-2">Assessment Tracking</h4>
              <p className="text-gray-600 text-sm">DISC, 16 Types, Enneagram, and OSHA assessments</p>
            </div>

            <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
              <div className="text-2xl mb-3">📋</div>
              <h4 className="font-semibold text-gray-800 mb-2">AI-Powered Summaries</h4>
              <p className="text-gray-600 text-sm">Intelligent personality summaries for employers</p>
            </div>

            <div className="bg-green-50 rounded-lg p-6 border border-green-200">
              <div className="text-2xl mb-3">🏗️</div>
              <h4 className="font-semibold text-gray-800 mb-2">Career Ready</h4>
              <p className="text-gray-600 text-sm">Preparing students for construction careers</p>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-gray-500 text-sm">
              Building careers, one student at a time.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
