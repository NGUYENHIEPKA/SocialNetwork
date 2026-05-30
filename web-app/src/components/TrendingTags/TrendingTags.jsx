import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchTrendingTags, selectTrendingTags, selectTrendingLoading } from "../../store/postsSlice";
import { Skeleton } from "../ui/skeleton.js";
import { TrendingUp } from "lucide-react";

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
      <div className="bg-muted rounded-lg p-4">
        <h3 className="font-semibold mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4" />
          Trending now
        </h3>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-10 w-full rounded-md" />
          ))}
        </div>
      </div>
    );
  }

  if (!tags || tags.length === 0) return null;

  return (
    <div className="bg-muted rounded-lg p-4">
      <h3 className="font-semibold mb-3 flex items-center gap-2">
        <TrendingUp className="w-4 h-4" />
        Trending now
      </h3>
      <div className="space-y-3">
        {tags.map((tag) => (
          <div
            key={tag}
            onClick={() => navigate(`/tag/${tag}`)}
            className="cursor-pointer hover:bg-background/50 p-2 rounded-md transition-colors"
          >
            <p className="text-sm text-muted-foreground">Very popular</p>
            <p className="font-medium text-primary">#{tag}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
