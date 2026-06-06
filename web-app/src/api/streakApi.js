import axios from "./axiosClient";

const streakApi = {
  // Lấy thông tin streak của một conversation
  getStreak: (conversationId) => {
    return axios.get(`/chat/streak/${conversationId}`);
  },

  // Khôi phục streak đã mất
  restoreStreak: (conversationId) => {
    return axios.post(`/chat/streak/${conversationId}/restore`);
  },
};

export default streakApi;
