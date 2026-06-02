import { rtkApi } from "./rtkApi";

export const rtkPostCommentApi = rtkApi.injectEndpoints({
  endpoints: (builder) => ({
    // GET Recommended Feed
    getRecommendedFeed: builder.query({
      query: ({ page = 0, size = 20 }) => ({
        url: `/posts/recommended?page=${page}&size=${size}`,
        method: "GET",
      }),
      providesTags: (result) =>
        result
          ? [
              ...result.map((post) => ({ type: "Post", id: post.id || post.postId })),
              { type: "Post", id: "LIST" },
            ]
          : [{ type: "Post", id: "LIST" }],
    }),

    // CREATE Post
    createPost: builder.mutation({
      query: (payload) => ({
        url: "/posts",
        method: "POST",
        data: payload,
      }),
      invalidatesTags: [{ type: "Post", id: "LIST" }],
    }),

    // DELETE Post
    deletePost: builder.mutation({
      query: (postId) => ({
        url: `/posts/${postId}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, postId) => [
        { type: "Post", id: postId },
        { type: "Post", id: "LIST" },
      ],
    }),

    // GET Comments
    getComments: builder.query({
      query: ({ postId, page = 0, size = 10 }) => ({
        url: `/comments/post/${postId}?page=${page}&size=${size}`,
        method: "GET",
      }),
      providesTags: (result, error, { postId }) =>
        result
          ? [
              ...result.map((comment) => ({ type: "Comment", id: comment.id })),
              { type: "Comment", id: `LIST-${postId}` },
            ]
          : [{ type: "Comment", id: `LIST-${postId}` }],
    }),

    // CREATE Comment
    createComment: builder.mutation({
      query: (payload) => ({
        url: "/comments",
        method: "POST",
        data: payload,
      }),
      invalidatesTags: (result, error, { postId }) => [
        { type: "Comment", id: `LIST-${postId}` },
        { type: "Post", id: postId }, // Cập nhật số lượng bình luận của bài viết
      ],
    }),

    // DELETE Comment
    deleteComment: builder.mutation({
      query: ({ postId, commentId }) => ({
        url: `/comments/${commentId}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, { postId, commentId }) => [
        { type: "Comment", id: commentId },
        { type: "Comment", id: `LIST-${postId}` },
        { type: "Post", id: postId },
      ],
    }),
  }),
});

export const {
  useGetRecommendedFeedQuery,
  useLazyGetRecommendedFeedQuery,
  useCreatePostMutation,
  useDeletePostMutation,
  useGetCommentsQuery,
  useCreateCommentMutation,
  useDeleteCommentMutation,
} = rtkPostCommentApi;
