import { Heart, MessageCircle, Repeat2 } from "lucide-react";
import { Button } from "../ui/button";
import { LikersTooltip } from "../LikersTooltip/LikersTooltip";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

export function PostActions({
  postId,
  isLiked,
  likes,
  commentCount,
  isReposted,
  reposts,
  liking,
  reposting,
  onLike,
  onCommentClick,
  onRepostAction,
}) {
  const [repostMenuOpen, setRepostMenuOpen] = useState(false);

  const formatNumber = (num) =>
    num >= 1_000_000
      ? (num / 1_000_000).toFixed(1) + "M"
      : num >= 1_000
      ? (num / 1_000).toFixed(1) + "K"
      : String(num);

  return (
    <div className="flex items-center gap-6 mt-2 py-1 select-none">
      {/* Nút Like kèm Bouncy Animation */}
      <LikersTooltip
        postId={postId}
        isLiked={isLiked}
        likes={likes}
        disabled={liking}
        onClick={(e) => {
          e.stopPropagation();
          onLike();
        }}
      >
        <div className="flex items-center group cursor-pointer">
          <motion.div
            whileTap={{ scale: 0.7 }}
            animate={{ scale: isLiked ? [1, 1.4, 1.2, 1] : 1 }}
            transition={{ duration: 0.35, ease: "easeOut" }}
          >
            <Heart
              className={`w-5 h-5 transition-colors duration-200 ${
                isLiked
                  ? "text-red-500 fill-red-500"
                  : "text-muted-foreground group-hover:text-red-500"
              }`}
            />
          </motion.div>
          <span
            className={`ml-1.5 text-xs font-semibold transition-colors duration-200 ${
              isLiked ? "text-red-500" : "text-muted-foreground group-hover:text-red-500"
            }`}
          >
            {formatNumber(likes)}
          </span>
        </div>
      </LikersTooltip>

      {/* Nút Bình luận */}
      <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
        <Button
          variant="ghost"
          size="sm"
          className="p-1 h-auto hover:bg-transparent group flex items-center cursor-pointer text-muted-foreground hover:text-blue-500 transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            onCommentClick();
          }}
        >
          <MessageCircle className="w-5 h-5" />
          <span className="ml-1.5 text-xs font-semibold">
            {formatNumber(commentCount)}
          </span>
        </Button>
      </motion.div>

      {/* Nút Repost Menu */}
      <DropdownMenu open={repostMenuOpen} onOpenChange={setRepostMenuOpen}>
        <DropdownMenuTrigger asChild>
          <div onClick={(e) => e.stopPropagation()}>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                variant="ghost"
                size="sm"
                className={`p-1 h-auto hover:bg-transparent group flex items-center cursor-pointer transition-colors ${
                  isReposted ? "text-green-500" : "text-muted-foreground hover:text-green-500"
                }`}
                aria-label="Repost"
              >
                <Repeat2 className="w-5 h-5" />
                <span className="ml-1.5 text-xs font-semibold">
                  {formatNumber(reposts)}
                </span>
              </Button>
            </motion.div>
          </div>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          align="start"
          sideOffset={8}
          className="w-40 bg-card border border-border/50 text-[14px] p-1 rounded-xl shadow-lg backdrop-blur-md bg-card/95"
          onClick={(e) => e.stopPropagation()}
        >
          <DropdownMenuItem
            className="cursor-pointer hover:bg-muted focus:bg-muted rounded-lg px-3 py-2 transition-colors font-medium"
            onClick={() => {
              onRepostAction();
              setRepostMenuOpen(false);
            }}
            disabled={reposting}
          >
            <div className="flex items-center justify-between w-full">
              <span className={isReposted ? "text-destructive" : "text-foreground"}>
                {isReposted ? "Hủy chia sẻ" : "Chia sẻ lại"}
              </span>
              <Repeat2 className={`w-4 h-4 ${isReposted ? "text-destructive" : "text-muted-foreground"}`} />
            </div>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
