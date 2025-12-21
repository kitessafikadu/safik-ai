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
