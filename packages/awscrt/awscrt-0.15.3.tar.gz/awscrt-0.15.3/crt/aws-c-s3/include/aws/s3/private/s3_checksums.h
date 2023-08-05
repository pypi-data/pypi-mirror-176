#ifndef AWS_S3_CHECKSUMS_H
#define AWS_S3_CHECKSUMS_H
/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0.
 */
#include "aws/s3/s3_client.h"

/* TODO: consider moving the aws_checksum_stream to aws-c-checksum, and the rest about checksum headers and trailer to
 * aws-c-sdkutil. */

struct aws_s3_checksum;

struct aws_checksum_vtable {
    void (*destroy)(struct aws_s3_checksum *checksum);
    int (*update)(struct aws_s3_checksum *checksum, const struct aws_byte_cursor *buf);
    int (*finalize)(struct aws_s3_checksum *checksum, struct aws_byte_buf *out, size_t truncate_to);
};

struct aws_s3_checksum {
    struct aws_allocator *allocator;
    struct aws_checksum_vtable *vtable;
    void *impl;
    size_t digest_size;
    enum aws_s3_checksum_algorithm algorithm;
    bool good;
};

struct checksum_config {
    enum aws_s3_checksum_location location;
    enum aws_s3_checksum_algorithm checksum_algorithm;
    bool validate_response_checksum;
    struct {
        bool crc32c;
        bool crc32;
        bool sha1;
        bool sha256;
    } response_checksum_algorithms;
};

/**
 * a stream that takes in a stream, computes a running checksum as it is read, and outputs the checksum when the stream
 * is destroyed.
 * Note: seek this stream will immediately fail, as it would prevent an accurate calculation of the
 * checksum.
 *
 * @param allocator
 * @param existing_stream The real content to read from. Destroying the checksum stream destroys the existing stream.
 *                        outputs the checksum of existing stream to checksum_output upon destruction. Will be kept
 *                        alive by the checksum stream
 * @param algorithm       Checksum algorithm to use.
 * @param checksum_output Checksum of the `existing_stream`, owned by caller, which will be calculated when this stream
 *                        is destroyed.
 */
AWS_S3_API
struct aws_input_stream *aws_checksum_stream_new(
    struct aws_allocator *allocator,
    struct aws_input_stream *existing_stream,
    enum aws_s3_checksum_algorithm algorithm,
    struct aws_byte_buf *checksum_output);

/**
 * TODO: properly support chunked encoding.
 *
 * A stream that takes in a stream, encodes it to aws_chunked. Computes a running checksum as it is read and add the
 * checksum as trailer at the end of the stream. All of the added bytes will be counted to the length of the stream.
 * Note: seek this stream will immediately fail, as it would prevent an accurate calculation of the
 * checksum.
 *
 * @param allocator
 * @param existing_stream   The data to be chunkified prepended by information on the stream length followed by a final
 *                          chunk and a trailing chunk containing a checksum of the existing stream. Destroying the
 *                          chunk stream will destroy the existing stream.
 * @param checksum_output   Optional argument, if provided the buffer will be initialized to the appropriate size and
 *                          filled with the checksum result when calculated. Callers responsibility to cleanup.
 */
AWS_S3_API
struct aws_input_stream *aws_chunk_stream_new(
    struct aws_allocator *allocator,
    struct aws_input_stream *existing_stream,
    enum aws_s3_checksum_algorithm algorithm,
    struct aws_byte_buf *checksum_output);

/**
 * Get the size of the checksum output corresponding to the aws_s3_checksum_algorithm enum value.
 */
AWS_S3_API
size_t aws_get_digest_size_from_algorithm(enum aws_s3_checksum_algorithm algorithm);

/**
 * Get the header name corresponding to the aws_s3_checksum_algorithm enum value.
 */
AWS_S3_API
const struct aws_byte_cursor *aws_get_http_header_name_from_algorithm(enum aws_s3_checksum_algorithm algorithm);

/**
 * Get the multipart upload header name corresponding to the aws_s3_checksum_algorithm enum value.
 */
AWS_S3_API
const struct aws_byte_cursor *aws_get_create_mpu_header_name_from_algorithm(enum aws_s3_checksum_algorithm algorithm);

/**
 * Get the complete multipart upload name corresponding to the aws_s3_checksum_algorithm enum value.
 */
AWS_S3_API
const struct aws_byte_cursor *aws_get_complete_mpu_name_from_algorithm(enum aws_s3_checksum_algorithm algorithm);

/**
 * create a new aws_checksum corresponding to the aws_s3_checksum_algorithm enum value.
 */
AWS_S3_API
struct aws_s3_checksum *aws_checksum_new(struct aws_allocator *allocator, enum aws_s3_checksum_algorithm algorithm);

/**
 * Compute an aws_checksum corresponding to the provided enum, passing a function pointer around instead of using a
 * conditional would be faster, but would be a negligble improvement compared to the cost of processing data twice
 * which would be the only time this function would be used, and would be harder to follow.
 */
AWS_S3_API
int aws_checksum_compute(
    struct aws_allocator *allocator,
    enum aws_s3_checksum_algorithm algorithm,
    const struct aws_byte_cursor *input,
    struct aws_byte_buf *output,
    size_t truncate_to);

/**
 * Cleans up and deallocates checksum.
 */
AWS_S3_API
void aws_checksum_destroy(struct aws_s3_checksum *checksum);

/**
 * Updates the running checksum with to_checksum. this can be called multiple times.
 */
AWS_S3_API
int aws_checksum_update(struct aws_s3_checksum *checksum, const struct aws_byte_cursor *to_checksum);

/**
 * Completes the checksum computation and writes the final digest to output.
 * Allocation of output is the caller's responsibility.
 */
AWS_S3_API
int aws_checksum_finalize(struct aws_s3_checksum *checksum, struct aws_byte_buf *output, size_t truncate_to);

AWS_S3_API
void checksum_config_init(struct checksum_config *internal_config, const struct aws_s3_checksum_config *config);

#endif /* AWS_S3_CHECKSUMS_H */
