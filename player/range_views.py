# -*- coding: utf-8 -*-
"""
支持 HTTP Range 请求的媒体文件视图
用于替代 Django 自带的 django.views.static.serve
"""

import os
import re
import mimetypes
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.conf import settings


def _file_iterator(file_path, start, length, chunk_size=64 * 1024):
    """流式读取文件指定范围"""
    with open(file_path, "rb") as f:
        f.seek(start)
        remaining = length
        while remaining > 0:
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:
                break
            yield chunk
            remaining -= len(chunk)


def serve_media(request, path):
    """支持 Range 的媒体文件视图"""
    # 1. 拼接物理路径 + 安全检查
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    file_path = os.path.abspath(os.path.join(media_root, path))

    # 防止路径穿越攻击
    if not file_path.startswith(media_root):
        raise Http404("Forbidden")

    if not os.path.isfile(file_path):
        raise Http404("File not found")

    file_size = os.path.getsize(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    # 2. 处理 Range 请求
    range_header = request.META.get("HTTP_RANGE", "").strip()

    if range_header:
        match = re.match(r"bytes=(\d*)-(\d*)", range_header)
        if not match:
            response = HttpResponse(status=416)
            response["Content-Range"] = f"bytes */{file_size}"
            return response

        start_str, end_str = match.groups()

        if start_str:
            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1
        else:
            # bytes=-500 表示最后 500 字节
            start = max(0, file_size - int(end_str))
            end = file_size - 1

        # 边界检查
        if start >= file_size or start > end:
            response = HttpResponse(status=416)
            response["Content-Range"] = f"bytes */{file_size}"
            return response

        end = min(end, file_size - 1)
        length = end - start + 1

        response = StreamingHttpResponse(
            _file_iterator(file_path, start, length),
            status=206,
            content_type=content_type,
        )
        response["Content-Length"] = str(length)
        response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response["Accept-Ranges"] = "bytes"
        response["Cache-Control"] = "no-cache"
        return response

    # 3. 无 Range：返回完整文件
    response = StreamingHttpResponse(
        _file_iterator(file_path, 0, file_size),
        content_type=content_type,
    )
    response["Content-Length"] = str(file_size)
    response["Accept-Ranges"] = "bytes"
    return response