package com.DuyHao.post_service.dto.response;

import java.util.List;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiTagResponse {
    private List<String> tags;
    private List<Double> scores;
}
