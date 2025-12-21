"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const navMenu = document.getElementById("navMenu");
      const hamburgerMenu = document.getElementById("hamburgerMenu");

      if (
        isOpen &&
        navMenu &&
        hamburgerMenu &&
        !navMenu.contains(event.target as Node) &&
        !hamburgerMenu.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [isOpen]);

  const isActive = (path: string) => {
    // For home sections, we might need more complex logic or just check if we are on home
    if (path.startsWith("#")) {
      return pathname === "/" ? "active" : "";
    }
    return pathname === path ? "active" : "";
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="nav-brand">
          <Link href="/" className="logo" onClick={closeMenu}>
            <svg
              width="32"
              height="32"
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect width="32" height="32" rx="6" fill="url(#gradient)" />
              <path
                d="M8 16L12 12L16 16L20 12L24 16"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <circle cx="12" cy="12" r="1.5" fill="white" />
              <circle cx="16" cy="16" r="1.5" fill="white" />
              <circle cx="20" cy="12" r="1.5" fill="white" />
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="32" y2="32">
                  <stop offset="0%" stopColor="#667eea" />
                  <stop offset="100%" stopColor="#764ba2" />
                </linearGradient>
              </defs>
            </svg>
            <span className="logo-text">Safik AI</span>
          </Link>
        </div>
        <button
          className={`hamburger-menu ${isOpen ? "active" : ""}`}
          id="hamburgerMenu"
          aria-label="Toggle menu"
          onClick={(e) => {
            e.stopPropagation();
            toggleMenu();
          }}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
        <ul className={`nav-menu ${isOpen ? "active" : ""}`} id="navMenu">
          <li>
            <Link
              href="/"
              className={pathname === "/" ? "active" : ""}
              onClick={closeMenu}
            >
              Home
            </Link>
          </li>
          <li>
            <Link href="/#services" onClick={closeMenu}>
              Services
            </Link>
          </li>
          <li>
            <Link href="/#about" onClick={closeMenu}>
              About
            </Link>
          </li>
          <li>
            <Link href="/#faq" onClick={closeMenu}>
              FAQ
            </Link>
          </li>
          <li>
            <Link
              href="/chatbot"
              className={`btn-chat ${pathname === "/chatbot" ? "active" : ""}`}
              onClick={closeMenu}
            >
              AI Chatbot
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
