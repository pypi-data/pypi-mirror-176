#ifndef AWS_IO_SOCKET_CHANNEL_HANDLER_H
#define AWS_IO_SOCKET_CHANNEL_HANDLER_H
/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0.
 */

#include <aws/io/io.h>

struct aws_socket;
struct aws_channel_handler;
struct aws_channel_slot;
struct aws_event_loop;

AWS_EXTERN_C_BEGIN
/**
 * Socket handlers should be the first slot/handler in a channel. It interacts directly with the channel's event loop
 * for read and write notifications. max_read_size is the maximum amount of data it will read from the socket
 * before a context switch (a continuation task will be scheduled).
 */
AWS_IO_API struct aws_channel_handler *aws_socket_handler_new(
    struct aws_allocator *allocator,
    struct aws_socket *socket,
    struct aws_channel_slot *slot,
    size_t max_read_size);

AWS_EXTERN_C_END

#endif /* AWS_IO_SOCKET_CHANNEL_HANDLER_H */
