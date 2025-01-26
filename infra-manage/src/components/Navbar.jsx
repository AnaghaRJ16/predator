import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const Navbar = () => (
  <nav className="flex justify-between items-center bg-gradient-to-r from-blue-500 to-green-500 text-white px-6 py-3 shadow-md">
    <div className="text-3xl font-extrabold">InfraManage</div>
    <div className="flex gap-6">
      <Link to="/resources" className="hover:text-gray-200">Resources</Link>
      <Link to="/projects" className="hover:text-gray-200">Projects</Link>
      <Link to="/analytics" className="hover:text-gray-200">Analytics</Link>
      <Link to="/team" className="hover:text-gray-200">Team</Link>
      <Link to="/contact" className="hover:text-gray-200">Contact</Link>
    </div>
    <div>
      <Button variant="ghost" className="text-white hover:text-gray-200">Log In</Button>
      <Button variant="outline" className="text-white border-white hover:bg-gray-200 hover:text-blue-600">Sign Up</Button>
    </div>
  </nav>
);

export default Navbar;
