"use client";

import { useEffect, useState, useRef } from "react";

interface CountUpProps {
  end: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
}

export default function CountUp({
  end,
  duration = 2000,
  prefix = "",
  suffix = "",
}: CountUpProps) {
  const [count, setCount] = useState(0);
  const elementRef = useRef<HTMLSpanElement>(null);
  const rafId = useRef<number | null>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (hasAnimated.current) {
      setCount(end);
      return;
    }

    let startTime: number | null = null;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;

      const progress = timestamp - startTime;
      const t = Math.min(progress / duration, 1);
      const ease = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

      setCount(Math.floor(ease * end));

      if (t < 1) {
        rafId.current = requestAnimationFrame(animate);
      } else {
        setCount(end);
        hasAnimated.current = true;
      }
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated.current) {
          rafId.current = requestAnimationFrame(animate);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (elementRef.current) observer.observe(elementRef.current);

    return () => {
      observer.disconnect();
      if (rafId.current) cancelAnimationFrame(rafId.current);
    };
  }, [end, duration]);

  return (
    <span ref={elementRef}>
      {prefix}{count}{suffix}
    </span>
  );
}
