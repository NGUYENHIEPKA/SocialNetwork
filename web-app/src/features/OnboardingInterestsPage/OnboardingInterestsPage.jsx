import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { 
  Cpu, Music, Compass, Utensils, Dumbbell, Sparkles, 
  Gamepad2, GraduationCap, Globe, Heart, Laugh, CloudRain, Flame, Check 
} from "lucide-react";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Spinner } from "../../components/ui/spinner";
import userApi from "../../api/userApi";
import { fetchMyInfo } from "../../store/userSlice";

const CATEGORY_METADATA = {
  tech_auto: { icon: Cpu, color: "from-blue-500/20 to-indigo-500/20", text: "text-blue-400", border: "border-blue-500/50", shadow: "shadow-blue-500/10" },
  entertainment: { icon: Music, color: "from-pink-500/20 to-purple-500/20", text: "text-pink-400", border: "border-pink-500/50", shadow: "shadow-pink-500/10" },
  travel_nature: { icon: Compass, color: "from-green-500/20 to-emerald-500/20", text: "text-green-400", border: "border-green-500/50", shadow: "shadow-green-500/10" },
  food_drink: { icon: Utensils, color: "from-yellow-500/20 to-amber-500/20", text: "text-amber-400", border: "border-amber-500/50", shadow: "shadow-amber-500/10" },
  sports: { icon: Dumbbell, color: "from-red-500/20 to-orange-500/20", text: "text-red-400", border: "border-red-500/50", shadow: "shadow-red-500/10" },
  fashion_beauty: { icon: Sparkles, color: "from-fuchsia-500/20 to-pink-500/20", text: "text-fuchsia-400", border: "border-fuchsia-500/50", shadow: "shadow-fuchsia-500/10" },
  gaming: { icon: Gamepad2, color: "from-violet-500/20 to-purple-500/20", text: "text-violet-400", border: "border-violet-500/50", shadow: "shadow-violet-500/10" },
  education: { icon: GraduationCap, color: "from-cyan-500/20 to-blue-500/20", text: "text-cyan-400", border: "border-cyan-500/50", shadow: "shadow-cyan-500/10" },
  news_society: { icon: Globe, color: "from-emerald-500/20 to-teal-500/20", text: "text-teal-400", border: "border-teal-500/50", shadow: "shadow-teal-500/10" },
  pets: { icon: Heart, color: "from-rose-500/20 to-pink-500/20", text: "text-rose-400", border: "border-rose-500/50", shadow: "shadow-rose-500/10" },
  vibe_funny: { icon: Laugh, color: "from-orange-500/20 to-yellow-500/20", text: "text-orange-400", border: "border-orange-500/50", shadow: "shadow-orange-500/10" },
  vibe_mood: { icon: CloudRain, color: "from-sky-500/20 to-indigo-500/20", text: "text-sky-400", border: "border-sky-500/50", shadow: "shadow-sky-500/10" },
  vibe_motivation: { icon: Flame, color: "from-amber-500/20 to-red-500/20", text: "text-red-400", border: "border-red-500/50", shadow: "shadow-red-500/10" }
};

export function OnboardingInterestsPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { profile } = useSelector((state) => state.user);

  const [interests, setInterests] = useState([]);
  const [selected, setSelected] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Fetch available interests from profile-service
  useEffect(() => {
    const fetchInterests = async () => {
      try {
        const res = await userApi.getAvailableInterests();
        if (res && res.code === 1000) {
          setInterests(res.result || []);
        } else {
          toast.error("Failed to load interests.");
        }
      } catch (err) {
        toast.error("Error loading onboarding categories.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchInterests();
  }, []);

  const handleToggle = (tag) => {
    if (selected.includes(tag)) {
      setSelected(selected.filter((item) => item !== tag));
    } else {
      setSelected([...selected, tag]);
    }
  };

  const handleSubmit = async () => {
    if (selected.length < 3) {
      toast.warning("Vui lòng chọn ít nhất 3 sở thích!");
      return;
    }

    try {
      setSubmitting(true);
      const res = await userApi.editProfile({ interests: selected });
      if (res && res.code === 1000) {
        toast.success("Đã lưu các sở thích của bạn!");
        await dispatch(fetchMyInfo()).unwrap();
        navigate("/feed", { replace: true });
      } else {
        toast.error("Lưu sở thích không thành công.");
      }
    } catch (err) {
      toast.error("Có lỗi xảy ra khi thiết lập sở thích.");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-white">
        <Spinner className="mb-4" />
        <p className="text-zinc-400 text-sm">Đang tải danh mục sở thích...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950 px-4 py-8 text-white">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-8">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl font-extrabold mb-2 tracking-tight text-white"
          >
            Chọn sở thích của bạn
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-zinc-400 text-base"
          >
            Chọn ít nhất 3 chủ đề bạn quan tâm để cá nhân hóa nguồn cấp dữ liệu của bạn.
          </motion.p>
        </div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.4 }}
          className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8"
        >
          {interests.map((item, idx) => {
            const meta = CATEGORY_METADATA[item.tag] || { icon: Globe, color: "from-zinc-800 to-zinc-900", text: "text-white", border: "border-zinc-700", shadow: "" };
            const IconComponent = meta.icon;
            const isSelected = selected.includes(item.tag);

            return (
              <motion.div
                key={item.tag}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleToggle(item.tag)}
                className={`relative group cursor-pointer p-5 rounded-2xl border transition-all duration-300 flex flex-col justify-between h-36 overflow-hidden ${
                  isSelected 
                    ? `bg-zinc-900 ${meta.border} shadow-lg ${meta.shadow}`
                    : "bg-zinc-900/40 border-zinc-800/80 hover:border-zinc-700"
                }`}
              >
                {/* Background glow decoration */}
                <div className={`absolute inset-0 bg-gradient-to-br ${meta.color} opacity-0 group-hover:opacity-40 transition-opacity duration-300`} />

                {/* Top header containing icon and checkbox */}
                <div className="flex justify-between items-start z-10">
                  <div className={`p-2.5 rounded-xl bg-zinc-800/70 border border-zinc-700/50 ${meta.text}`}>
                    <IconComponent className="w-6 h-6" />
                  </div>

                  <div className={`w-6 h-6 rounded-full border flex items-center justify-center transition-all ${
                    isSelected 
                      ? "bg-white border-white" 
                      : "border-zinc-700 group-hover:border-zinc-500"
                  }`}>
                    {isSelected && <Check className="w-3.5 h-3.5 text-black stroke-[3]" />}
                  </div>
                </div>

                {/* Title */}
                <div className="z-10 mt-4">
                  <h3 className="font-semibold text-sm leading-tight text-zinc-100 group-hover:text-white transition-colors">
                    {item.displayName.split(" / ")[1] || item.displayName}
                  </h3>
                  <span className="text-zinc-500 text-xs mt-0.5 block">
                    {item.displayName.split(" / ")[0]}
                  </span>
                </div>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Action Panel */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="flex flex-col sm:flex-row items-center justify-between p-6 rounded-3xl bg-zinc-900/50 border border-zinc-800/60 backdrop-blur-xl gap-4"
        >
          <div className="text-center sm:text-left">
            <p className="text-sm text-zinc-400">
              Đã chọn: <span className="font-bold text-white text-lg">{selected.length}</span> / 3
            </p>
            {selected.length < 3 && (
              <p className="text-xs text-zinc-500 mt-1">Chọn thêm {3 - selected.length} chủ đề nữa</p>
            )}
          </div>

          <Button
            size="lg"
            className="w-full sm:w-auto px-8 rounded-xl font-bold bg-white text-black hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:shadow-none transition-all duration-300 shadow-md shadow-white/5"
            disabled={selected.length < 3 || submitting}
            onClick={handleSubmit}
          >
            {submitting ? (
              <>
                <Spinner className="mr-2 w-4 h-4" /> Đang thiết lập...
              </>
            ) : (
              "Bắt đầu khám phá"
            )}
          </Button>
        </motion.div>
      </div>
    </div>
  );
}
