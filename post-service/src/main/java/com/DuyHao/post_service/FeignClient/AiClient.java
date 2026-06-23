package com.DuyHao.post_service.FeignClient;

import com.DuyHao.post_service.dto.request.AiTagRequest;
import com.DuyHao.post_service.dto.response.AiTagResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "ai-service", url = "${app.service.ai}")
public interface AiClient {

    @PostMapping("/internal/ai/extract-tags")
    AiTagResponse extractTags(@RequestBody AiTagRequest request);
}
