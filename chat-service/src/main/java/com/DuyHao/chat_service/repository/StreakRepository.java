package com.DuyHao.chat_service.repository;

import com.DuyHao.chat_service.entity.Streak;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StreakRepository extends MongoRepository<Streak, String> {

    Optional<Streak> findByConversationId(String conversationId);

    // Tìm streak có lastStreakDate < date để kiểm tra mất streak
    List<Streak> findAllByLastStreakDateBeforeOrLastStreakDateIsNull(String date);

    List<Streak> findAllByRestoreResetMonthNot(String currentMonth);
}
