"""
Content Moderator — phát hiện nội dung nhạy cảm trong bài đăng mạng xã hội.

Phân loại:
  profanity      — từ tục tĩu, chửi thề
  hate_speech    — kỳ thị, phân biệt đối xử
  violence       — đe dọa, kêu gọi bạo lực
  adult_content  — nội dung người lớn, tình dục
  personal_info  — thông tin cá nhân (SĐT, CCCD, tài khoản ngân hàng)
  spam           — quảng cáo, spam, lừa đảo

Mức cảnh báo:
  safe      — không phát hiện vấn đề
  mild      — có thể gây hiểu lầm, nên cân nhắc
  moderate  — chứa nội dung nhạy cảm, cần chỉnh sửa
  severe    — vi phạm nghiêm trọng, không nên đăng
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Từ điển nhạy cảm

_PROFANITY: List[str] = [
    # ── Viết tắt chửi thề tiếng Việt ──────────────────────────────────────
    "đmm", "đm", "đkm", "đcm", "dmm", "dm", "vl", "vkl",
    "clgt", "clm", "đl", "đll", "wtf", "stfu", "omfg",
    "vcl", "vlz", "vcll", "vlon", "vlin", "vloz", "vailol", "vailoz",
    "cmm", "cmnr", "cmnl", "dmcs", "dmcc", "đmcs", "đcmm", "đkmm",
    "đệt", "đệt mẹ", "đệt cha", "đệt con", "đệch", "đệch mẹ",
    "đếch", "đếch biết", "đếch hiểu", "đếch cần", "đếch quan tâm",
    "đếk", "đếk biết", "đếk hiểu",
    "vlxx", "vl loz", "vl đỉnh", "vl thật", "vl thiệt",
    "lozz", "lozzz", "loz",
    # ── Câu chửi đầy đủ tiếng Việt ────────────────────────────────────────
    "mẹ kiếp", "mẹ mày", "tiên sư mày", "tiên sư cha mày",
    "cha mày", "má mày", "bố mày chết", "đồ con hoang",
    "đồ mả cha", "mả cha mày", "mả mẹ mày",
    "cút xéo", "cút đi", "xéo đi", "biến đi",
    # ── Xúc phạm cá nhân tiếng Việt ───────────────────────────────────────
    "chó chết", "thằng chó", "con chó", "đồ chó", "như chó",
    "đồ khốn", "thằng khốn", "con khốn", "đồ khốn nạn", "khốn nạn",
    "đồ ngu", "thằng ngu", "con ngu", "ngu như bò", "ngu như chó",
    "ngu vl", "ngu xuẩn", "ngu dốt", "ngu ngốc", "ngu si",
    "đồ điên", "thằng điên", "con điên", "điên khùng",
    "đồ chết", "mày chết đi", "đồ súc vật", "đồ mất dạy",
    "đĩ thúi", "gái điếm", "đồ điếm", "cave bẩn",
    "đồ rác", "đồ bỏ đi", "rác rưởi", "cặn bã", "đồ phế",
    "vô dụng", "vô học", "vô lại", "hèn hạ", "hèn mạt",
    "đần độn", "óc lợn", "não cá vàng", "não bã đậu",
    "đầu óc bã đậu", "nói chuyện như chó",
    # ── Từ tục tiếng Việt ──────────────────────────────────────────────────
    "địt", "địt mẹ", "địt cha", "cặc", "lồn", "buồi",
    "đụ", "đụ mẹ", "đụ má", "đụ cha",
    "dume", "đụmẹ", "duma", "đụmá", "ducha", "đụcha",
    "ditme", "địtmẹ", "ditcha", "địtcha", "ditmemay",
    "cackho", "concack", "concac",
    "đjt", "djt",
    "đéo",
    # ── Từ xúc phạm đứng độc lập (word-boundary) ──────────────────────────
    "ngu", "khốn", "điên", "đần", "ngốc",
    "hèn", "dốt", "tởm", "ghê tởm",
    # ── Tiếng Anh — chửi thề / tục tĩu ───────────────────────────────────
    "fuck", "fucking", "fucker", "fck", "f*ck", "fuk",
    "shit", "bullshit", "shitty", "sht",
    "bitch", "son of a bitch", "sob",
    "asshole", "ass", "bastard", "dumbass",
    "crap", "damn", "dammit", "hell",
    "motherfucker", "mf", "mfer",
    "dick", "cock", "pussy", "cunt",
    "whore", "slut", "hoe",
    "jackass", "idiot", "moron", "retard", "stupid",
    "loser", "jerk", "douche", "douchebag",
    "piss off", "get lost", "go to hell", "shut up",
    "screw you", "go fuck yourself",
]

_HATE_SPEECH: List[str] = [
    # ── Kỳ thị chủng tộc / sắc tộc (VI) ──────────────────────────────────
    "mọi rợ", "man di mọi rợ", "dân mọi", "mọi đen",
    "dân da đen", "bọn da đen", "đồ da đen",
    "dân tàu", "đồ tàu khựa", "tàu khựa",
    "mán", "thằng mán", "đồ mán",
    # ── Kỳ thị vùng miền (VI) ─────────────────────────────────────────────
    "dân tỉnh lẻ quê mùa", "dân quê mùa", "dân nhà quê",
    "đồ miền quê", "bắc kỳ", "nam kỳ", "trung kỳ", "mọi miền núi",
    # ── Kỳ thị giới tính / LGBT+ (VI) ─────────────────────────────────────
    "pê đê", "bê đê", "lại cái", "bóng lộ",
    "đồng tính bệnh hoạn", "gay bệnh", "les bệnh",
    "người chuyển giới bệnh hoạn", "tranny",
    "đàn bà mà làm lãnh đạo", "phụ nữ không biết lái xe",
    "đàn bà vào bếp đi", "phụ nữ chỉ biết nội trợ",
    # ── Kỳ thị tôn giáo (VI) ──────────────────────────────────────────────
    "đạo giả", "tà đạo", "đạo hồi khủng bố", "bọn theo đạo",
    # ── Xúc phạm nhóm người (VI) ──────────────────────────────────────────
    "người già vô dụng", "người tàn tật vô dụng", "người khuyết tật ăn hại",
    "đám ăn hại", "bọn nghèo hèn", "đám dốt nát", "bọn thất học",
    "người béo đáng bị ghét", "đồ mập xấu xí",
    "phụ nữ không đáng được tôn trọng", "đàn bà chỉ là đồ vật",
    # ── Body/appearance shaming (VI) ──────────────────────────────────────
    # Béo / mập
    "béo như lợn", "béo như heo", "béo ú", "béo ục ịch", "đồ béo phì",
    "mập như heo", "mập như lợn", "mập ú", "đồ mập ú",
    "heo nái", "con heo nái",
    # Gầy / ốm
    "gầy như que", "gầy như que củi", "gầy trơ xương", "ốm nhom ốm nhách",
    "ốm như cò", "ốm như que",
    # Lùn
    "đồ lùn", "thằng lùn", "con lùn", "lùn tịt", "lùn xủn", "lùn như nấm",
    # Xấu / mặt
    "xấu như ma", "xấu như quỷ", "mặt như khỉ", "mặt như heo",
    "mặt như chó", "mặt kinh dị", "xấu kinh dị", "xấu hoắc",
    "đồ xấu xí", "mặt mẹt",
    # ── Age shaming (VI) ──────────────────────────────────────────────────
    "già cú đế", "già khú đế", "già hết thời", "bà già lú lẫn",
    "ông già lú lẫn", "ông già lẩm cẩm", "bà già lẩm cẩm",
    "đồ già nua", "lão già", "lão khốn", "mụ già",
    # Tiếng Anh — body shaming
    "ugly as hell", "ugly af", "fat pig", "fat cow", "fat ass",
    "you are fat", "fatso", "lard ass",
    "ugly bitch", "ugly motherfucker",
    "midget", "shorty bitch",
    "boomer trash", "old hag", "old fart",
    # ── Tiếng Anh — hate speech ───────────────────────────────────────────
    "nigger", "nigga", "negro",
    "chink", "gook", "spic", "wetback", "kike", "towelhead",
    "white trash", "redneck",
    "faggot", "fag", "dyke", "tranny", "shemale",
    "women belong in kitchen", "go back to your country",
    "white supremacy", "ethnic cleansing", "kill all",
    "inferior race", "subhuman",
    "all muslims are terrorists", "all jews are",
    "disabled people are useless", "retards should be",
]

_VIOLENCE: List[str] = [
    # ── Imperative ngắn — đe dọa / xúi giục chết ─────────────────────────
    # Bắt được cả viết tắt leet "gi3t di", "ch3t di"
    "giết đi", "chết đi", "tự sát đi", "tự tử đi",
    "giết mình đi", "tự giết đi", "đi chết đi",
    # ── Đe dọa trực tiếp (VI) ─────────────────────────────────────────────
    "tao giết mày", "tao sẽ giết", "tao giết chết", "tao định giết",
    "giết mày", "bắn mày", "thịt mày",
    "chémmày", "giếtmày", "đâmmày", "bắnmày", "đánhmày", "xửmày",
    "mày sẽ chết", "mày chết đi", "cho mày chết", "mày không sống được đâu",
    # Biến thể "chếc" (c thay t cuối): mày chếc đi, chếc mẹ mày
    "mày chếc", "mày chếc đi", "chếc mẹ mày", "chếc cha mày",
    "tao chém mày", "tao sẽ chém", "chém mày", "chém chết mày", "cho mày ăn dao",
    "tao đánh mày", "tao sẽ đánh", "đánh mày", "đánh đến chết", "đánh chết mày",
    "tao xử mày", "xử đẹp mày", "tao sẽ xử", "sẽ xử mày", "xử mày",
    "tao hành mày", "hành mày", "ra đây tao đánh", "đợi tao ra đó",
    "tao bắn mày", "tao sẽ bắn", "bắn chết", "tao thịt mày",
    "đập tan xác", "băm xác", "chặt đầu", "chặt tay",
    "tạt axit", "đổ axit lên", "thiêu sống",
    "đâm chết", "đâm mày", "cầm dao đâm", "rút dao đâm",
    # ── Từ hành động nguy hiểm đứng độc lập ──────────────────────────────
    "chém", "đâm", "bắn", "thiêu", "tạt axit",
    # Biến thể không dấu / dấu giả: che'm, che`m, chem — đều normalize về "chem".
    "chem",
    # ── Viết tắt
    "t giết m", "tao giết m", "t giết mày",
    "t đập m", "tao đập m", "t đập mày",
    "t chết m", "t cho m chết", "t cho mày chết",
    "t đánh m", "tao đánh m", "t đánh mày",
    "t xử m", "tao xử m", "t xử mày",
    "t bắn m", "tao bắn m", "t bắn mày",
    "t chém m", "tao chém m", "t chém mày",
    "t đâm m", "tao đâm m", "t đâm mày",
    "t thịt m", "tao thịt m", "t thịt mày",
    "t hành m", "tao hành m", "t hành mày",
    # ── Kêu gọi bạo lực nhóm (VI) ────────────────────────────────────────
    "đánh chết bọn", "giết hết bọn", "tiêu diệt bọn",
    "đánh hội đồng", "kéo nhau đi đánh", "rủ nhau đi đánh",
    "ném đá vào", "đốt nhà", "đốt xe", "phá nhà",
    "đập phá", "cướp", "hành hung",
    # ── Hành động nguy hiểm / máu me ──────────────────────────────────────
    "máu me", "chảy máu", "đổ máu", "giết người",
    "chém người", "băng đảng", "giang hồ xử nhau",
    "thanh toán nhau", "thanh trừng", "thủ tiêu",
    "bắt cóc", "tống tiền", "cướp của", "giết người cướp của",
    "tra tấn", "hành hạ", "bạo hành",
    # ── Tự làm hại bản thân (VI) ──────────────────────────────────────────
    "tự tử thôi", "muốn tự tử", "sẽ tự tử",
    "không muốn sống nữa", "muốn chết đi", "chán sống",
    "sẽ kết thúc tất cả", "lấy tính mạng", "kết liễu",
    "tự cắt tay", "tự làm đau bản thân",
    # ── Cyberbullying / xúi giục tự hại (VI) ──────────────────────────────
    "tự xử đi", "tự xử cho rồi", "tự xử cho xong",
    "biến khỏi mạng", "biến khỏi facebook", "out khỏi đời",
    "đừng sống nữa", "chết đi cho rồi", "chết quách cho xong",
    "cút khỏi đây", "cút khỏi mạng",
    # ── Doxing / đe dọa phát tán (VI) ─────────────────────────────────────
    "tao biết nhà mày", "tao biết địa chỉ mày", "tao biết chỗ ở mày",
    "tao biết số điện thoại mày", "tao biết trường mày",
    "tao sẽ tung ảnh", "tao sẽ phát tán ảnh", "tao sẽ tung clip",
    "đăng ảnh sỉ nhục", "đăng clip sỉ nhục",
    "tung tin nhắn riêng", "leak tin nhắn", "leak ảnh riêng",
    "doxing", "doxxing", "deanon mày",
    # ── Tiếng Anh — threats & violence ───────────────────────────────────
    "i will kill you", "i'll kill you", "gonna kill",
    "i will hurt you", "you will die", "you're dead",
    "i will stab", "i will shoot", "gonna shoot",
    "beat you up", "beat the shit", "smash your face",
    "burn your house", "blow up", "bomb threat",
    "want to die", "want to kill myself", "going to end it",
    "suicide", "self harm", "cut myself",
    "kill them all", "wipe them out",
    "shoot up", "mass shooting", "school shooting",
    "terrorist attack", "blow myself up",
    "murder", "slaughter", "massacre",
]

_ADULT_CONTENT: List[str] = [
    # ── Từ ngữ tình dục tiếng Việt ────────────────────────────────────────
    "khiêu dâm", "phim khiêu dâm", "nội dung khiêu dâm",
    "phim sex", "video sex", "clip sex", "ảnh sex",
    "ảnh nude", "ảnh nóng", "clip nóng", "video nóng",
    "gái gọi", "trai gọi", "dịch vụ tình dục",
    "mua dâm", "bán dâm", "mại dâm",
    "massage kích dục", "massage tình dục", "massage happy ending",
    "tìm bạn qua đêm", "ngủ qua đêm có thù lao",
    "quan hệ tình dục", "làm tình", "giao cấu",
    "sờ soạng", "sàm sỡ", "quấy rối tình dục",
    "hiếp dâm", "cưỡng hiếp", "xâm hại tình dục",
    "ấu dâm", "xâm hại trẻ em",
    "dâm ô", "dâm dục", "trụy lạc",
    "phim người lớn", "nội dung 18+",
    # ── Tiếng Anh — adult content ─────────────────────────────────────────
    "porn", "pornography", "xxx",
    "nude photo", "nude video", "naked picture",
    "sex tape", "sex video", "adult film",
    "prostitution", "escort service", "call girl",
    "one night stand for money", "sugar daddy arrangement",
    "sexual harassment", "rape", "sexual assault",
    "child abuse", "child pornography", "pedophile", "cp",
    "molest", "grope",
    "nsfw", "onlyfans leak", "leaked nudes",
    "hookup for cash", "pay for sex",
]

_DRUGS: List[str] = [
    # ── Ma túy đá / methamphetamine (VI) ──────────────────────────────────
    "hàng đá", "đá xanh", "đá tinh thể", "ma túy đá",
    "ngáo đá", "lên đá", "đập đá", "chơi đá",
    "bay đá",
    # ── Heroin / hàng trắng (VI) ──────────────────────────────────────────
    "hàng trắng", "bột trắng", "chích choác", "chích heroin",
    "tép trắng", "tép vàng", "cắn tép",
    # ── Ketamine / ke (VI) ────────────────────────────────────────────────
    "chơi ke", "ke đêm", "ke đá", "phê ke",
    # ── Cần sa / marijuana (VI) ───────────────────────────────────────────
    "cần sa", "cỏ mỹ", "hút cỏ", "cuốn cỏ", "cuốn cần",
    "lá cần", "bồ đà", "thuốc lào tẩm",
    # ── Thuốc lắc / MDMA (VI) ─────────────────────────────────────────────
    "thuốc lắc", "viên lắc", "bay lắc", "đi bay", "đập lắc",
    "lắc đêm", "kẹo lắc",
    # ── GHB / nước vui (VI) ───────────────────────────────────────────────
    "nước vui", "thuốc kích dục",
    # ── Bóng cười / shisha có chất ────────────────────────────────────────
    "bóng cười", "shisha bay", "shisha có hàng",
    # ── Buôn bán / sử dụng (VI) ───────────────────────────────────────────
    "mua ma túy", "bán ma túy", "buôn ma túy", "shop ma túy",
    "ship hàng đá", "giao hàng đá", "kèo bay",
    "phê pha", "chơi thuốc", "bay đêm cùng",
    # ── Tiếng Anh — drug terms ────────────────────────────────────────────
    "marijuana", "weed", "ganja", "pot weed",
    "cocaine", "crack cocaine", "snort coke",
    "heroin", "smack heroin",
    "meth", "methamphetamine", "crystal meth", "ice meth",
    "ecstasy pill", "mdma", "molly pill",
    "lsd trip", "acid trip", "acid tab",
    "shroom", "magic mushroom", "psilocybin",
    "fentanyl", "ketamine k",
    "drug dealer", "selling drugs", "buying drugs", "drug pusher",
    "get high", "getting high on", "smoking weed",
]

_GAMBLING: List[str] = [
    # ── Cá độ thể thao (VI) ───────────────────────────────────────────────
    "cá độ bóng đá", "cá độ thể thao", "cá độ tennis", "cá cược bóng đá",
    "kèo bóng", "kèo châu á", "kèo châu âu", "kèo tài xỉu",
    "ăn kèo", "bể kèo", "kèo thơm", "kèo vip", "kèo nội bộ",
    "tip xanh chín", "tip kèo",
    # ── Lô đề / xổ số chui (VI) ───────────────────────────────────────────
    "lô đề", "đánh đề", "ghi đề", "chốt đề", "đầu đề", "đuôi đề",
    "lô tô chui", "đánh lô", "ghi lô", "chốt lô",
    "soi cầu", "dàn đề", "dàn lô", "dàn xíu", "dàn 4 số",
    "lô xiên", "đề xiên",
    # ── Bài bạc (VI) ──────────────────────────────────────────────────────
    "tài xỉu", "xóc đĩa", "ba cây", "tiến lên ăn tiền",
    "phỏm ăn tiền", "đánh phỏm tiền", "đánh bạc online",
    "sòng bài online", "sòng bạc online", "casino online", "casino lậu",
    "baccarat online", "blackjack tiền", "roulette online",
    "slot game tiền", "nổ hũ", "game nổ hũ",
    # ── Đá gà ─────────────────────────────────────────────────────────────
    "đá gà online", "đá gà trực tuyến", "đá gà cựa sắt online",
    "cá độ đá gà",
    # ── Nhà cái / link cược (VI) ──────────────────────────────────────────
    "nhà cái uy tín", "đại lý nhà cái", "link nhà cái",
    "link cá độ", "link cược uy tín", "link cược nhanh",
    "nạp tiền nhà cái", "rút tiền nhà cái", "hoàn tiền cược",
    # ── Tiếng Anh — gambling ──────────────────────────────────────────────
    "online casino", "sports betting site", "place a bet",
    "betting site", "betting tips", "betting kèo",
    "poker for money", "blackjack for money", "slot machine online",
    "bookmaker site", "odds betting",
]

_SPAM_PATTERNS: List[str] = [
    # ── Kiếm tiền nhanh / đa cấp (VI) ────────────────────────────────────
    "kiếm tiền online dễ dàng", "kiếm triệu mỗi ngày",
    "kiếm tiền không cần làm việc", "thu nhập khủng tại nhà",
    "làm giàu nhanh chóng", "bí quyết làm giàu",
    "kinh doanh đa cấp", "mô hình kim tự tháp",
    "đầu tư 0 rủi ro", "lợi nhuận 100%", "cam kết hoàn vốn",
    "lãi suất cao bất thường", "lãi 30% mỗi tháng",
    "tiền ảo đảm bảo lãi", "crypto đảm bảo sinh lời",
    "forex uy tín cam kết", "sàn forex hoàn tiền",
    # ── Lừa đảo (VI) ──────────────────────────────────────────────────────
    "bạn đã trúng thưởng", "bạn trúng thưởng", "chúc mừng bạn trúng",
    "nhấp vào link", "nhấp link", "click link", "click vào link",
    "nhận quà ngay", "nhận thưởng ngay", "click nhận thưởng ngay",
    "nhận iphone miễn phí", "nhận xe máy miễn phí",
    "nhận tiền mặt ngay", "quà tặng hấp dẫn chờ bạn",
    "nạp tiền nhận bonus khủng", "cá độ uy tín hoàn tiền",
    "link cược uy tín", "xổ số online uy tín",
    "hack tài khoản ngân hàng", "hack tiền điện thoại",
    "thẻ cào miễn phí", "nạp thẻ miễn phí",
    # ── Spam bán hàng / hàng giả (VI) ────────────────────────────────────
    "hàng nhái y hệt hàng thật", "hàng fake chất lượng cao",
    "thuốc giảm cân thần kỳ", "giảm cân không cần ăn kiêng",
    "thuốc tăng cường sinh lý", "thuốc cường dương",
    "thuốc ngoài luồng", "thuốc không rõ nguồn gốc",
    "mua followers", "tăng like ảo", "view ảo giá rẻ",
    # ── App vay nóng / tín dụng đen (VI) ──────────────────────────────────
    "vay tiền online", "vay tiền nhanh online", "vay tiền không thế chấp",
    "vay không cần cccd", "vay không cần thẩm định", "vay không cần gặp mặt",
    "app vay nóng", "app vay tiền nhanh", "vay nóng giải ngân ngay",
    "giải ngân trong ngày", "duyệt vay 24/7", "vay 5 triệu nhận liền",
    "tín dụng đen", "vay tiền bùng được",
    # ── Romance scam (VI) ─────────────────────────────────────────────────
    "muốn gửi quà cho em", "muốn gửi tiền cho em",
    "đóng phí hải quan", "đóng phí nhận quà", "đóng phí thông quan",
    "kiện hàng bị giữ", "kiện hàng đang bị giữ",
    # ── Giả mạo / phishing (VI) ───────────────────────────────────────────
    "tài khoản bị khóa", "tài khoản bị tạm khóa", "xác minh tài khoản ngay",
    "xác thực tài khoản gấp", "xác minh otp", "cung cấp otp",
    "bưu phẩm chưa giao", "bưu phẩm bị giữ", "click nhận bưu phẩm",
    "shipper giao hàng giả", "giả mạo shipper",
    "đơn hàng có vấn đề", "đơn hàng bị lỗi click",
    "thông báo từ ngân hàng click", "thông báo cqdt", "công an điều tra liên hệ",
    # ── Tiếng Anh — scam mở rộng ──────────────────────────────────────────
    "loan no credit check", "instant loan no document",
    "payday loan fast", "borrow money no collateral",
    "i am a us soldier", "i am an army general",
    "send me money for shipping", "pay customs fee",
    "your account is locked", "verify your account immediately",
    "verify your otp", "share your otp",
    "your package is held", "click to release your package",
    "irs final notice", "fbi investigation contact",
    # ── Tiếng Anh — spam / scam ───────────────────────────────────────────
    "click here to claim", "you have won", "congratulations you won",
    "free iphone", "free gift", "claim your prize", "limited time offer",
    "make money fast", "make money online easy", "earn money from home",
    "earn fast cash", "passive income guaranteed", "financial freedom fast",
    "investment with guaranteed return", "zero risk investment",
    "guaranteed profit", "100% profit", "risk free investment",
    "buy followers", "buy likes cheap", "fake views", "buy real followers",
    "pyramid scheme", "mlm opportunity", "get rich quick", "quick money",
    "wire transfer scam", "nigerian prince", "send me money",
    "your account has been compromised", "verify your account now",
    "click the link below to win", "you are selected", "lucky winner",
    "lose weight fast", "miracle diet pill", "lose 10kg in 1 week",
    "magic weight loss", "diet pill no exercise",
    "enlargement pill", "male enhancement", "sexual performance pill",
]

# Regex để phát hiện thông tin cá nhân
_PERSONAL_INFO_PATTERNS: List[Tuple[str, str, str]] = [
    # (pattern, category_label, description)
    (
        # SĐT VN bắt đầu bằng 0: 9-11 chữ số (bao gồm di động 10 số + cố định)
        r"\b0\d{8,10}\b",
        "phone_number",
        "Số điện thoại",
    ),
    (
        r"\b\d{9}\b",
        "id_card",
        "Có thể là số CMND (9 chữ số)",
    ),
    (
        r"\b\d{12}\b",
        "id_card",
        "Có thể là số CCCD (12 chữ số)",
    ),
    (
        r"\b[0-9]{6,20}\b(?=.*(?:tài khoản|tk|stk|số tài khoản|account))",
        "bank_account",
        "Số tài khoản ngân hàng",
    ),
    (
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        "email",
        "Địa chỉ email",
    ),
]

# Cấu hình mức cảnh báo

# category → mức tối thiểu khi phát hiện
_CATEGORY_SEVERITY: Dict[str, str] = {
    "profanity":     "mild",
    "hate_speech":   "moderate",
    "violence":      "severe",
    "adult_content": "severe",
    "personal_info": "moderate",
    "spam":          "mild",
    "drugs":         "severe",
    "gambling":      "moderate",
}

_LEVEL_ORDER = ["safe", "mild", "moderate", "severe"]

_CATEGORY_LABELS_VI: Dict[str, str] = {
    "profanity":     "Profanity / Swearing",
    "hate_speech":   "Hate speech / Discrimination",
    "violence":      "Violence / Threats",
    "adult_content": "Adult content",
    "personal_info": "Personal information",
    "spam":          "Advertising / Spam",
    "drugs":         "Drugs / Illegal substances",
    "gambling":      "Gambling / Betting",
}

_WARNING_MESSAGES: Dict[str, str] = {
    "safe":     "Your post looks good to go.",
    "mild":     "Your post contains some potentially inappropriate language. Please review before posting.",
    "moderate": "Your post contains sensitive content. Please edit before posting.",
    "severe":   "Your post violates community guidelines. This content cannot be posted.",
}

# Kết quả phát hiện

@dataclass
class FlaggedItem:
    word: str
    category: str
    category_label: str
    severity: str


@dataclass
class ModerationResult:
    is_safe: bool
    warning_level: str                        # safe / mild / moderate / severe
    categories: List[str]                     # danh sách category vi phạm
    flagged_items: List[FlaggedItem]
    message: str
    suggestion: str


# Chuẩn hóa văn bản — dual mode

# Dấu giả ASCII (', `, ^, ~) gắn sau nguyên âm
_FAKE_TONE_RE = re.compile(r"([aeiouyAEIOUY])[\'`\^~]+")

# Biến thể chính tả phổ biến (áp dụng SAU khi đã bỏ dấu tiếng Việt).
_PHONETIC_RE_SUBS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"iec\b"), "iet"),
    (re.compile(r"iek\b"), "iet"),
]

_LEET_SUBS: Dict[str, str] = {
    "@": "a", "0": "o", "1": "i", "3": "e",
    "4": "a", "5": "s", "7": "t", "8": "b", "$": "s",
    "*": "", "!": "",
}


def _strip_diacritics(text: str) -> str:
    """Bỏ dấu tiếng Việt + đ/Đ → d."""
    text = text.replace("đ", "d").replace("Đ", "d")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def _normalize_soft(text: str) -> str:
    """Chuẩn hóa nhẹ — giữ dấu tiếng Việt."""
    text = unicodedata.normalize("NFC", text)
    text = text.lower().strip()
    text = _FAKE_TONE_RE.sub(r"\1", text)
    for k, v in _LEET_SUBS.items():
        text = text.replace(k, v)
    # Bỏ punctuation chèn giữa từ để né lọc: d.m, gi.ết, đ-m, đ_m, d·m, d/m, d:m
    text = re.sub(r"(?<=\w)[.\-_·•/|:](?=\w)", "", text, flags=re.UNICODE)
    # Ghép các từ 1-ký-tự liên tiếp thành 1 chuỗi
    text = re.sub(
        r"\b(?:\w\s+){2,}\w\b",
        lambda m: m.group(0).replace(" ", ""),
        text,
        flags=re.UNICODE,
    )
    text = re.sub(r"(.)\1+", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text

# Phone normalization — chuyển chữ số tiếng Việt + bỏ separator giữa số

_VI_NUM_WORDS: Dict[str, str] = {
    "không": "0",
    "một": "1", "mốt": "1",
    "hai": "2",
    "ba": "3",
    "bốn": "4", "tư": "4",
    "năm": "5", "lăm": "5", "nhăm": "5",
    "sáu": "6",
    "bảy": "7", "bẩy": "7",
    "tám": "8",
    "chín": "9",
}

_VI_NUM_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _VI_NUM_WORDS) + r")\b",
    re.IGNORECASE | re.UNICODE,
)


def _normalize_phone(text: str) -> str:
    """
    Sinh phiên bản content dành riêng cho regex SĐT/CCCD/...:
      - Chuyển chữ số tiếng Việt ("không", "chín", ...) → digit
      - Bỏ separator (space/dot/dash/slash/...) GIỮA hai chữ số
      → bắt được "0 chín bảy 5 4 5 5 8 8 2" và "0.1234-3939"
    """
    text = unicodedata.normalize("NFC", text).lower()
    text = _VI_NUM_RE.sub(lambda m: _VI_NUM_WORDS[m.group(1).lower()], text)
    text = re.sub(r"(?<=\d)[\s.\-_·•/|:()]+(?=\d)", "", text)
    return text


def _normalize(text: str) -> str:
    """Chuẩn hóa mạnh = soft + strip dấu tiếng Việt + phonetic."""
    text = _normalize_soft(text)
    text = _strip_diacritics(text)
    for pat, repl in _PHONETIC_RE_SUBS:
        text = pat.sub(repl, text)
    return text


def _use_soft_mode(soft_normalized: str) -> bool:
    """Từ ngắn (≤4 ký tự) đứng độc lập dùng soft mode để tránh
    va chạm với từ tiếng Việt thông thường sau khi strip diacritics."""
    return 0 < len(soft_normalized) <= 4 and " " not in soft_normalized


def _build_pattern(normalized: str, soft_mode: bool) -> Optional[re.Pattern]:
    if not normalized:
        return None

    boundary = r"[a-zA-ZÀ-ỹ\d]" if soft_mode else r"[a-z\d]"
    parts = normalized.split()

    if len(parts) == 1:
        escaped = re.escape(normalized)
        pattern = rf"(?<!{boundary}){escaped}(?!{boundary})"
        return re.compile(pattern, re.IGNORECASE | re.UNICODE)

    if len(parts) == 3:
        a, b, c = (re.escape(p) for p in parts)
        GAP = r"(?:\s+\S+){0,2}\s+"
        pattern = a + GAP + b + GAP + c
    elif len(parts) == 2:
        a, b = (re.escape(p) for p in parts)
        GAP = r"(?:\s+\S+){0,2}\s+"
        pattern = a + GAP + b
    else:
        escaped = re.escape(normalized)
        pattern = re.sub(r"\\ ", r"[\\s]+", escaped)

    return re.compile(pattern, re.IGNORECASE | re.UNICODE)


# Pre-compile tất cả pattern một lần
# Mỗi entry: (compiled_pattern, original_word, soft_mode_flag)
_WORD_LISTS: Dict[str, List[str]] = {
    "profanity":    _PROFANITY,
    "hate_speech":  _HATE_SPEECH,
    "violence":     _VIOLENCE,
    "adult_content": _ADULT_CONTENT,
    "spam":         _SPAM_PATTERNS,
    "drugs":        _DRUGS,
    "gambling":     _GAMBLING,
}

_CompiledEntry = Tuple[re.Pattern, str, bool]
_COMPILED: Dict[str, List[_CompiledEntry]] = {}

for _cat, _words in _WORD_LISTS.items():
    seen: set = set()
    entries: List[_CompiledEntry] = []
    for _w in _words:
        _soft = _normalize_soft(_w)
        _soft_mode = _use_soft_mode(_soft)
        _normalized = _soft if _soft_mode else _normalize(_w)
        _key = (_normalized, _soft_mode)
        if not _normalized or _key in seen:
            continue
        seen.add(_key)
        _pat = _build_pattern(_normalized, _soft_mode)
        if _pat is not None:
            entries.append((_pat, _w, _soft_mode))
    _COMPILED[_cat] = entries

_COMPILED_PERSONAL = [
    (re.compile(pat, re.IGNORECASE), label, desc)
    for pat, label, desc in _PERSONAL_INFO_PATTERNS
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _bump_level(current: str, new: str) -> str:
    """Trả về mức cao hơn giữa current và new."""
    return _LEVEL_ORDER[max(_LEVEL_ORDER.index(current), _LEVEL_ORDER.index(new))]


def moderate(content: str, strict: bool = False) -> ModerationResult:
    """
    Kiểm tra nội dung bài đăng.

    Args:
        content:  Văn bản cần kiểm tra.
        strict:   True → cảnh báo cả mức "mild" (không đăng được);
                  False → chỉ cảnh báo, người dùng tự quyết định.

    Returns:
        ModerationResult với đầy đủ thông tin cảnh báo.
    """
    soft_text = _normalize_soft(content)
    full_text = _normalize(content)
    flagged: List[FlaggedItem] = []
    seen_words: set = set()

    # 1. Kiểm tra từ điển — chọn target text theo mode của pattern
    for cat, patterns in _COMPILED.items():
        for pattern, original_word, soft_mode in patterns:
            target = soft_text if soft_mode else full_text
            if pattern.search(target):
                if original_word not in seen_words:
                    seen_words.add(original_word)
                    flagged.append(FlaggedItem(
                        word=original_word,
                        category=cat,
                        category_label=_CATEGORY_LABELS_VI[cat],
                        severity=_CATEGORY_SEVERITY[cat],
                    ))

    # 2. Kiểm tra thông tin cá nhân — chạy regex trên cả text gốc lẫn
    #    phone-normalized (đã chuyển chữ số tiếng Việt và bỏ separator).
    phone_text = _normalize_phone(content)
    for pattern, label, desc in _COMPILED_PERSONAL:
        for target in (content, phone_text):
            match = pattern.search(target)
            if not match:
                continue
            matched_text = match.group(0)
            key = f"personal_info:{matched_text}"
            if key not in seen_words:
                seen_words.add(key)
                flagged.append(FlaggedItem(
                    word=matched_text,
                    category="personal_info",
                    category_label=f"{_CATEGORY_LABELS_VI['personal_info']} ({desc})",
                    severity=_CATEGORY_SEVERITY["personal_info"],
                ))
            break

    # 3. Tính mức cảnh báo tổng hợp
    warning_level = "safe"
    for item in flagged:
        warning_level = _bump_level(warning_level, item.severity)

    # 4. Danh sách category duy nhất
    categories = list(dict.fromkeys(item.category for item in flagged))

    # 5. Xác định is_safe
    if strict:
        is_safe = (warning_level == "safe")
    else:
        is_safe = warning_level in ("safe", "mild")

    # 6. Thông điệp + gợi ý
    message = _WARNING_MESSAGES[warning_level]
    suggestion = _build_suggestion(categories, warning_level)

    return ModerationResult(
        is_safe=is_safe,
        warning_level=warning_level,
        categories=categories,
        flagged_items=flagged,
        message=message,
        suggestion=suggestion,
    )


def _build_suggestion(categories: List[str], level: str) -> str:
    """Build specific suggestions based on violation categories."""
    if not categories:
        return "Your post is ready to publish!"

    tips = []
    if "profanity" in categories:
        tips.append("Replace profanity with more respectful language.")
    if "hate_speech" in categories:
        tips.append("Remove discriminatory or hateful language.")
    if "violence" in categories:
        tips.append("Remove threatening or violent content.")
    if "adult_content" in categories:
        tips.append("Adult content is not allowed on this platform.")
    if "personal_info" in categories:
        tips.append("Consider removing sensitive personal information (phone, ID, email).")
    if "spam" in categories:
        tips.append("Remove advertising or potentially fraudulent content.")
    if "drugs" in categories:
        tips.append("Content promoting or referencing illegal drugs is not allowed.")
    if "gambling" in categories:
        tips.append("Gambling or betting promotion is not allowed on this platform.")

    return " ".join(tips)
