package com.DuyHao.chat_service.dto.response;

import lombok.*;
import lombok.experimental.FieldDefaults;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
public class StreakResponse {

    int streakCount;
    String lastStreakDate;
    boolean iSentToday;
    boolean partnerSentToday;
    boolean canRestore;
    String canRestoreUntil;
    int brokenStreakCount;
    int restoreRemaining; // số lần khôi phục còn lại
}
