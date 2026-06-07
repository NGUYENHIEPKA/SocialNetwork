package com.DuyHao.chat_service.service;

import com.DuyHao.chat_service.dto.RealtimeMessage;
import com.DuyHao.chat_service.dto.response.MessageResponse;
import com.DuyHao.chat_service.entity.Message;
import com.DuyHao.chat_service.repository.MessageRepository;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

/**
 * Service chuyên xử lý system message — không phụ thuộc vào MessageService hay StreakService
 * để tránh circular dependency.
 * Dùng chung cho: streak events, rời nhóm, kick thành viên, v.v.
 */
@Slf4j
@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class SystemMessageService {

    MessageRepository messageRepository;
    RedisPublisherService redisPublisherService;

    /**
     * Lưu một system message vào DB và đẩy realtime tới room.
     *
     * @param conversationId ID của conversation
     * @param content        Nội dung hiển thị
     * @param type           Loại message, ví dụ: SYSTEM_STREAK_LOST, SYSTEM_LEFT_GROUP, SYSTEM_KICKED...
     */
    public void send(String conversationId, String content, String type) {
        try {
            Message sysMsg = Message.builder()
                    .conversationId(conversationId)
                    .senderId("SYSTEM")
                    .content(content)
                    .type(type)
                    .createdAt(LocalDateTime.now())
                    .build();
            sysMsg = messageRepository.save(sysMsg);

            MessageResponse payload = MessageResponse.builder()
                    .id(sysMsg.getId())
                    .conversationId(conversationId)
                    .content(sysMsg.getContent())
                    .type(sysMsg.getType())
                    .createdAt(sysMsg.getCreatedAt())
                    .isMe(false)
                    .build();

            RealtimeMessage rtMessage = RealtimeMessage.builder()
                    .toRoomId(conversationId)
                    .type("message")
                    .payload(payload)
                    .build();

            redisPublisherService.publish(rtMessage);

            log.info("[SYSTEM_MSG] Gửi '{}' ({}) tới conversation {}", content, type, conversationId);
        } catch (Exception e) {
            log.error("[SYSTEM_MSG] Lỗi gửi system message tới conversation {}: {}", conversationId, e.getMessage());
        }
    }
}
