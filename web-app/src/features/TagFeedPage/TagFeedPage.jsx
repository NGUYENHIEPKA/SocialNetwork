import { useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { PostCard } from "../../components/PostCard/PostCard.jsx";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchPostsByTag,
  resetTagFeed,
  selectTagPosts,
  selectTagHasMore,
  selectTagPostsLoading,
  selectTagPage,
} from "../../store/postsSlice";
import { toast } from "sonner";
import { ChevronLeft } from "lucide-react";
import { Button } from "../../components/ui/button.js";

export function TagFeedPage() {
  const { tagName } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const posts = useSelector(selectTagPosts);
  const hasMore = useSelector(selectTagHasMore);
  const loading = useSelector(selectTagPostsLoading);
  const page = useSelector(selectTagPage);

  const loadMoreRef = useRef(null);
  const loadDelayRef = useRef(null);

  // Reset and fetch initial posts when tag changes
  useEffect(() => {
    dispatch(resetTagFeed());
    dispatch(fetchPostsByTag({ tag: tagName, page: 0, size: 20 }))
      .unwrap()
      .catch(() => toast.error("Failed to load posts for #" + tagName));
  }, [dispatch, tagName]);

  // Infinite scroll
  useEffect(() => {
    if (!hasMore || loading) return;

    const el = loadMoreRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (!entry.isIntersecting) return;
        if (loading || !hasMore) return;

        if (loadDelayRef.current) return;

        loadDelayRef.current = setTimeout(() => {
          dispatch(fetchPostsByTag({ tag: tagName, page, size: 20 }))
            .unwrap()
            .catch(() => toast.error("Failed to load more posts"));
          loadDelayRef.current = null;
        }, 300);
      },
      { root: null, threshold: 0.1 }
    );

    observer.observe(el);

    return () => observer.disconnect();
  }, [hasMore, loading, page, dispatch, tagName]);

  const handleProfileClick = (username) => {
    navigate(`/profile/@${username}`);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="border-b border-border p-4 bg-background/80 backdrop-blur-sm sticky top-0 z-10 flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
          <ChevronLeft className="w-6 h-6" />
        </Button>
        <h2 className="text-xl font-semibold">#{tagName}</h2>
      </div>

      <div className="min-h-screen">
        {posts.map((post) => {
          const username = post.username ?? post.user?.username ?? "unknown";
          const fullName = post.fullName ?? post.user?.fullName ?? "User";
          const avatarUrl = post.avatarUrl ?? post.user?.avatarUrl;
          const createdAt = post.createdAt ?? post.created_time ?? post.created_at;
          const mediaList = Array.isArray(post.mediaUrls) ? post.mediaUrls : [];

          return (
            <PostCard
              key={post.id}
              post={{
                ...post,
                username,
                fullName,
                avatarUrl,
                createdAt,
                mediaList,
              }}
              onProfileClick={handleProfileClick}
              onPostClick={(id) => navigate(`/post/${id}`)}
            />
          );
        })}

        {posts.length === 0 && !loading && (
          <div className="p-10 text-center text-muted-foreground">
            No posts found with this tag.
          </div>
        )}
      </div>

      <div className="p-4 text-center">
        {loading && hasMore && (
          <span className="text-muted-foreground text-sm">Loading...</span>
        )}
        {hasMore && <div ref={loadMoreRef} className="h-1" />}
        {!hasMore && posts.length > 0 && (
          <span className="text-muted-foreground text-sm">No more posts</span>
        )}
      </div>
    </div>
  );
}
