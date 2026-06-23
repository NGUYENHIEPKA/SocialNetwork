package com.DuyHao.post_service.dto.request;

import java.util.List;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiTagRequest {
    private String content;
    private List<String> imageUrls;
    private Double threshold;
}
