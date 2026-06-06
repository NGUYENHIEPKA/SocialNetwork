import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchTrendingTags, selectTrendingTags, selectTrendingLoading } from "../../store/postsSlice";
import { Skeleton } from "../ui/skeleton.js";
import { TrendingUp } from "lucide-react";
import { motion } from "framer-motion";


export function TrendingTags() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const tags = useSelector(selectTrendingTags);
  const loading = useSelector(selectTrendingLoading);

  useEffect(() => {
    dispatch(fetchTrendingTags(3));
  }, [dispatch]);

  if (loading) {
    return (
      <div className="bg-card/45 backdrop-blur-md rounded-2xl border border-border/30 p-4 shadow-sm relative overflow-hidden">
        {/* Glow decoration */}
        <div className="absolute -top-10 -right-10 w-24 h-24 bg-violet-500/10 blur-2xl rounded-full pointer-events-none" />
        
        <h3 className="font-semibold text-sm text-foreground/90 mb-3 flex items-center gap-2 relative z-10">
          <TrendingUp className="w-4 h-4 stroke-[1.5] text-violet-500" />
          Trending now
        </h3>
        <div className="space-y-2.5 relative z-10">
          {[1, 2, 3].map((i) => (
            <div key={i} className="p-2.5 rounded-xl border border-border/20 bg-muted/20 animate-pulse space-y-1.5 h-[50px] flex flex-col justify-center">
              <div className="h-3.5 w-1/2 bg-muted/40 rounded" />
              <div className="h-2.5 w-1/3 bg-muted/30 rounded" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!tags || tags.length === 0) return null;

  return (
    <div className="bg-card/45 backdrop-blur-md rounded-2xl border border-border/30 p-4 shadow-sm relative overflow-hidden">
      {/* Glow decoration */}
      <div className="absolute -top-10 -right-10 w-24 h-24 bg-violet-500/10 blur-2xl rounded-full pointer-events-none" />
      
      <h3 className="font-semibold text-sm text-foreground/90 mb-3 flex items-center gap-2 relative z-10">
        <TrendingUp className="w-4 h-4 stroke-[1.5] text-violet-500" />
        Trending now
      </h3>
      <div className="space-y-2 relative z-10">
        {tags.map((tag) => (
          <motion.div
            key={tag}
            whileHover={{ x: 4, scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={() => navigate(`/tag/${tag}`)}
            className="cursor-pointer hover:bg-muted/30 p-2.5 rounded-xl border border-transparent hover:border-border/30 flex items-center justify-between transition-all duration-300 group"
          >
            <div className="min-w-0">
              <p className="font-semibold text-sm text-foreground/95 group-hover:text-violet-400 transition-colors truncate">
                #{tag}
              </p>
              <p className="text-[10px] text-muted-foreground mt-0.5">Very popular</p>
            </div>
            <div className="w-6 h-6 shrink-0 rounded-full bg-violet-500/10 flex items-center justify-center border border-violet-500/20 text-violet-400 text-xs shadow-sm group-hover:scale-110 transition-transform">
              🔥
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

