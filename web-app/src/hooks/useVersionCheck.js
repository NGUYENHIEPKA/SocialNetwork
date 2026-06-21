import { useEffect, useRef } from 'react';
import { toast } from 'sonner';

// Version được inject lúc build bởi Vite
const CURRENT_VERSION = typeof __APP_VERSION__ !== 'undefined' ? __APP_VERSION__ : 'dev';

export function useVersionCheck() {
  const toastShownRef = useRef(false);

  useEffect(() => {
    // Bỏ qua khi dev local
    if (CURRENT_VERSION === 'dev') return;

    const check = async () => {
      try {
        const res = await fetch('/version.json?t=' + Date.now());
        if (!res.ok) return;

        const { version } = await res.json();

        if (version !== CURRENT_VERSION && !toastShownRef.current) {
          toastShownRef.current = true;
          toast.info('Có phiên bản mới! Bạn có muốn cập nhật không?', {
            duration: Infinity,
            action: {
              label: 'Cập nhật ngay',
              onClick: () => window.location.reload(),
            },
            cancel: {
              label: 'Để sau',
              onClick: () => {
                toastShownRef.current = false; // cho hiện lại lần check sau
              },
            },
          });
        }
      } catch {
        // Bỏ qua lỗi network
      }
    };

    // Check lần đầu sau 1 phút (chờ app ổn định)
    const timeout = setTimeout(check, 60_000);
    // Sau đó check mỗi 5 phút
    const interval = setInterval(check, 5 * 60_000);

    return () => {
      clearTimeout(timeout);
      clearInterval(interval);
    };
  }, []);
}
