import { createApi } from "@reduxjs/toolkit/query/react";
import axiosClient from "./axiosClient";

// Custom base query using the existing axiosClient to reuse interceptors & refresh token logic
const axiosBaseQuery =
  ({ baseUrl } = { baseUrl: "" }) =>
  async ({ url, method, data, params, headers }) => {
    try {
      const result = await axiosClient({
        url: baseUrl + url,
        method,
        data,
        params,
        headers,
      });
      // axiosClient response interceptor returns response.data directly
      return { data: result?.result || result };
    } catch (axiosError) {
      const err = axiosError;
      return {
        error: {
          status: err.response?.status || 500,
          data: err.response?.data || err.message || "Đã xảy ra lỗi hệ thống",
        },
      };
    }
  };

export const rtkApi = createApi({
  reducerPath: "rtkApi",
  baseQuery: axiosBaseQuery({ baseUrl: "" }),
  tagTypes: ["Post", "Comment", "Story", "User"],
  endpoints: () => ({}), // Endpoints will be injected or defined directly
});
