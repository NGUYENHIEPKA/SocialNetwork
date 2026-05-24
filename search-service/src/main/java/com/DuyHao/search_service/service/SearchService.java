package com.DuyHao.search_service.service;

import com.DuyHao.search_service.FeignClient.PostClient;
import com.DuyHao.search_service.FeignClient.ProfileClient;
import com.DuyHao.search_service.dto.response.PostResponse;
import com.DuyHao.search_service.dto.response.SearchResponse;
import com.DuyHao.search_service.dto.response.UserProfileResponse;
import java.util.Collections;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class SearchService {

    private final ProfileClient profileClient;
    private final PostClient postClient;

    public SearchResponse search(String keyword, int page, int size) {
        List<UserProfileResponse> users = Collections.emptyList();
        List<PostResponse> posts = Collections.emptyList();

        try {
            users = profileClient.searchUsers(keyword);
            log.info("Search users with keyword [{}] returned {} results", keyword, users.size());
        } catch (Exception e) {
            log.error("Error calling profile-service.searchUsers(keyword={}): {}", keyword, e.getMessage(), e);
        }

        try {
            posts = postClient.searchPosts(keyword, page, size);
            log.info("Search posts with keyword [{}] returned {} results", keyword, posts.size());
        } catch (Exception e) {
            log.error("Error calling post-service.searchPosts(keyword={}): {}", keyword, e.getMessage(), e);
        }

        return SearchResponse.builder().users(users).posts(posts).build();
    }

    public List<UserProfileResponse> searchUsers(String keyword) {
        try {
            return profileClient.searchUsers(keyword);
        } catch (Exception e) {
            log.error("Error calling profile-service.searchUsers(keyword={}): {}", keyword, e.getMessage(), e);
            return Collections.emptyList();
        }
    }

    public List<PostResponse> searchPosts(String keyword, int page, int size) {
        try {
            return postClient.searchPosts(keyword, page, size);
        } catch (Exception e) {
            log.error("Error calling post-service.searchPosts(keyword={}): {}", keyword, e.getMessage(), e);
            return Collections.emptyList();
        }
    }
}
