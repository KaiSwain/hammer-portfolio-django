export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-2">🔨</span>
              <h3 className="text-lg font-semibold">If I Had A Hammer</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Empowering the next generation of skilled tradespeople through 
              comprehensive pre-apprenticeship training and assessment.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-md font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-300">
              <li><a href="/login" className="hover:text-white transition-colors">Teacher Portal</a></li>
              <li><a href="/admin" className="hover:text-white transition-colors">Admin Panel</a></li>
              <li><span className="text-gray-400">Student Portal (Coming Soon)</span></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-md font-semibold mb-4">Contact</h4>
            <div className="space-y-2 text-sm text-gray-300">
              <p>📧 support@ifihadahammer.edu</p>
              <p>📞 (555) 123-HAMMER</p>
              <p>🏗️ Building careers, one student at a time</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2025 If I Had A Hammer. All rights reserved. | 
            <span className="ml-2">Built for educational excellence in construction trades</span>
          </p>
        </div>
      </div>
    </footer>
  );
}
