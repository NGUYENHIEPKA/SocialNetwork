package com.DuyHao.chat_service.entity;

import lombok.*;
import lombok.experimental.FieldDefaults;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Document(collection = "streaks")
public class Streak {

    @Id
    String id;

    @Indexed(unique = true)
    String conversationId;

    String userAId;
    String userBId;
    int streakCount;

    boolean userASentToday;
    boolean userBSentToday;
    String lastStreakDate;      // Ngày cuối cùng streak tăng
    String lastActivityDate;    // Ngày cuối cùng có tin nhắn
    int brokenStreakCount;      // streak trước khi mất
    String canRestoreUntil;     // Hạn chót có thể khôi phục

    // Số lần đã dùng khôi phục trong tháng này (tối đa 3 lần)
    @Builder.Default
    int restoreUsedThisMonth = 0;

    // Tháng được track để reset restoreUsedThisMonth về 0
    String restoreResetMonth;
}
