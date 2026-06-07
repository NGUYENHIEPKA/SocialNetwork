package com.DuyHao.chat_service.repository;

import com.DuyHao.chat_service.entity.Message;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MessageRepository extends MongoRepository<Message, String> {
    Page<Message> findAllByConversationIdOrderByCreatedAtDesc(String conversationId, Pageable pageable);
    Optional<Message> findFirstByConversationIdAndSenderIdOrderByCreatedAtDesc(String conversationId, String senderId);
}
