package com.DuyHao.chat_service.controller;

import com.DuyHao.chat_service.dto.ApiResponse;
import com.DuyHao.chat_service.dto.response.StreakResponse;
import com.DuyHao.chat_service.service.StreakService;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/streak")
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class StreakController {

    StreakService streakService;

    @GetMapping("/{conversationId}")
    ApiResponse<StreakResponse> getStreak(@PathVariable String conversationId) {
        return ApiResponse.<StreakResponse>builder()
                .result(streakService.getStreak(conversationId))
                .build();
    }

    @PostMapping("/{conversationId}/restore")
    ApiResponse<StreakResponse> restoreStreak(@PathVariable String conversationId) {
        return ApiResponse.<StreakResponse>builder()
                .result(streakService.restoreStreak(conversationId))
                .build();
    }
}
