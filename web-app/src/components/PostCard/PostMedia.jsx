import { useState, useMemo, useEffect, useRef } from "react";

export function PostMedia({ mediaList, mediaCount, onMediaClick }) {
  const multiSize = useMemo(() => {
    if (mediaCount <= 1) return null;
    if (mediaCount === 2) return { width: 250, height: 300 };
    return { width: 180, height: 250 };
  }, [mediaCount]);

  const mediaScrollRef = useRef(null);
  const isDraggingRef = useRef(false);
  const startXRef = useRef(0);
  const scrollLeftRef = useRef(0);
  const hasDraggedRef = useRef(false);

  useEffect(() => {
    const handleUp = () => {
      const el = mediaScrollRef.current;
      if (!isDraggingRef.current || !el) return;
      isDraggingRef.current = false;
      el.classList.remove("cursor-grabbing");
    };

    window.addEventListener("mouseup", handleUp);
    window.addEventListener("mouseleave", handleUp);

    return () => {
      window.removeEventListener("mouseup", handleUp);
      window.removeEventListener("mouseleave", handleUp);
    };
  }, []);

  const handleMediaMouseDown = (e) => {
    if (!mediaScrollRef.current) return;
    if (e.button !== 0) return;

    const el = mediaScrollRef.current;
    isDraggingRef.current = true;
    hasDraggedRef.current = false;
    el.classList.add("cursor-grabbing");

    startXRef.current = e.pageX - el.offsetLeft;
    scrollLeftRef.current = el.scrollLeft;
  };

  const handleMediaMouseMove = (e) => {
    const el = mediaScrollRef.current;
    if (!isDraggingRef.current || !el) return;
    e.preventDefault();
    const x = e.pageX - el.offsetLeft;
    const walk = x - startXRef.current;
    if (Math.abs(walk) > 5) {
      hasDraggedRef.current = true;
    }
    el.scrollLeft = scrollLeftRef.current - walk;
  };

  const containerRef = useRef(null);
  useEffect(() => {
    const root = containerRef.current;
    if (!root) return;

    const videos = root.querySelectorAll("video[data-autoplay]");
    if (!videos.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const el = entry.target;
          if (entry.isIntersecting && entry.intersectionRatio >= 0.7) {
            el.play().catch(() => {});
          } else {
            el.pause();
          }
        });
      },
      { threshold: [0, 0.7, 1] }
    );

    videos.forEach((el) => {
      el.muted = true;
      el.playsInline = true;
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, [mediaCount]);

  if (mediaCount === 0) return null;

  return (
    <div ref={containerRef} className="mt-3 flex justify-center w-full">
      {mediaCount === 1 ? (
        (() => {
          const m = mediaList[0];
          const url = m.mediaUrl;
          const isVideo = m.mediaType === "video";

          if (isVideo) {
            return (
              <video
                src={url}
                loop
                data-autoplay
                className="rounded-2xl border border-border/30 object-contain shadow-md cursor-pointer"
                style={{
                  maxWidth: "min(680px, 100%)",
                  maxHeight: "420px",
                  width: "auto",
                  height: "auto",
                  backgroundColor: "#000",
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onMediaClick?.(0);
                }}
              />
            );
          }

          return (
            <div 
              className="overflow-hidden rounded-2xl border border-border/30 shadow-md cursor-pointer"
              style={{
                maxWidth: "min(680px, 100%)",
                maxHeight: "420px",
              }}
            >
              <img
                src={url}
                alt="Post media"
                className="object-contain transition-transform duration-500 hover:scale-[1.03]"
                style={{
                  maxWidth: "100%",
                  maxHeight: "420px",
                  width: "auto",
                  height: "auto",
                }}
                loading="lazy"
                onClick={(e) => {
                  e.stopPropagation();
                  onMediaClick?.(0);
                }}
              />
            </div>
          );
        })()
      ) : (
        <div className="w-full flex justify-center">
          <div className="relative w-full max-w-[680px]">
            <div
              ref={mediaScrollRef}
              onMouseDown={handleMediaMouseDown}
              onMouseMove={handleMediaMouseMove}
              onDragStart={(e) => e.preventDefault()}
              className="post-media-scroll overflow-x-auto cursor-grab py-1 flex gap-3 select-none"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex gap-3 w-max mx-auto px-2">
                {mediaList.map((m, idx) => {
                  const url = /^https?:\/\//i.test(m.mediaUrl)
                    ? m.mediaUrl
                    : `${import.meta.env.VITE_BACKEND_URL || ""}${m.mediaUrl}`;
                  const isVideo = m.mediaType === "video";

                  return (
                    <div
                      key={m.id ?? idx}
                      className="relative flex-shrink-0 rounded-2xl overflow-hidden border border-border/30 bg-black shadow-md cursor-pointer group"
                      style={{
                        width: multiSize?.width ?? 240,
                        height: multiSize?.height ?? 340,
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        if (hasDraggedRef.current) return;
                        onMediaClick?.(idx);
                      }}
                    >
                      {isVideo ? (
                        <video
                          src={url}
                          loop
                          data-autoplay
                          className="w-full h-full object-cover rounded-2xl transition-transform duration-500 group-hover:scale-105"
                        />
                      ) : (
                        <img
                          src={url}
                          alt={`Post media multiple ${idx}`}
                          className="w-full h-full object-cover rounded-2xl transition-transform duration-500 group-hover:scale-105"
                          loading="lazy"
                        />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
