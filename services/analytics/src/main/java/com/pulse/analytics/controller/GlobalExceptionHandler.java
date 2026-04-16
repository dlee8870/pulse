package com.pulse.analytics.controller;

import com.pulse.analytics.dto.ErrorResponse;
import com.pulse.analytics.exception.ResourceNotFoundException;
import jakarta.servlet.http.HttpServletRequest;
import java.time.OffsetDateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/** Maps exceptions to consistent API error responses. */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(
            ResourceNotFoundException ex,
            HttpServletRequest request
    ) {
        return build(HttpStatus.NOT_FOUND, "not_found", ex.getMessage(), request.getRequestURI());
    }

    @ExceptionHandler({MethodArgumentNotValidException.class, HttpMessageNotReadableException.class})
    public ResponseEntity<ErrorResponse> handleBadRequest(
            Exception ex,
            HttpServletRequest request
    ) {
        return build(HttpStatus.BAD_REQUEST, "bad_request", "Invalid request payload.", request.getRequestURI());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpectedException(
            Exception ex,
            HttpServletRequest request
    ) {
        logger.error("Unhandled exception", ex);
        return build(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "internal_error",
                "Internal server error.",
                request.getRequestURI()
        );
    }

    private ResponseEntity<ErrorResponse> build(
            HttpStatus status,
            String error,
            String message,
            String path
    ) {
        return ResponseEntity.status(status).body(new ErrorResponse(
                OffsetDateTime.now(),
                status.value(),
                error,
                message,
                path
        ));
    }
}
