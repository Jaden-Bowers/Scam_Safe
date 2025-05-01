// Logo and title header

import React from "react";

function Header() {
  return (
    <header className="w-full py-4 flex justify-center items-center">
      <div className="flex items-center space-x-2">
        <img
          src="/logo.svg"
          alt="Scam Safe Logo"
          className="w-12 h-12"
        />
        <h2 className="text-4xl">
          <span className="text-white">Scam</span>
          <span className="text-[#0054FF]"> Safe</span>
        </h2>
      </div>
    </header>
  );
}

export default Header;
