from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


@dataclass
class ImageEntry:
    path: str
    pixmap: QPixmap
    cv_image: np.ndarray


def load_image_entries(paths: Iterable[str]) -> List[ImageEntry]:
    entries: List[ImageEntry] = []
    for path in paths:
        entry = _load_image_entry(path)
        if entry is not None:
            entries.append(entry)
    return entries


def convert_images(
    images: List[np.ndarray],
    threshold: int,
    aspect_w: int,
    aspect_h: int,
    margin_percent: float,
    output_folder: Optional[str] = None,
) -> Tuple[List[np.ndarray], List[str]]:
    if not images:
        return [], []

    prepared = [_ensure_bgra(img) for img in images]
    global_box = find_alpha_bounds(prepared, threshold)
    if any(v is None for v in global_box):
        h, w = prepared[0].shape[:2]
        global_box = (0, w, 0, h)

    outputs = crop_images_aspect_ratio(
        prepared,
        global_box,
        aspect_w=aspect_w,
        aspect_h=aspect_h,
        margin_percent=margin_percent,
    )

    saved_paths: List[str] = []
    if output_folder:
        out_dir = Path(output_folder)
        out_dir.mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(outputs):
            out_path = out_dir / f"frame_{i + 1:02d}.png"
            cv2.imwrite(str(out_path), img)
            saved_paths.append(str(out_path))

    return outputs, saved_paths


def pixmap_from_bgr(image: np.ndarray) -> QPixmap:
    if image.ndim == 2:
        qimg = QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            image.strides[0],
            QImage.Format_Grayscale8,
        )
        return QPixmap.fromImage(qimg.copy())

    if image.shape[2] == 4:
        rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        qimg = QImage(
            rgba.data,
            rgba.shape[1],
            rgba.shape[0],
            rgba.strides[0],
            QImage.Format_RGBA8888,
        )
    else:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimg = QImage(
            rgb.data,
            rgb.shape[1],
            rgb.shape[0],
            rgb.strides[0],
            QImage.Format_RGB888,
        )

    return QPixmap.fromImage(qimg.copy())


def find_alpha_bounds(
    images: List[np.ndarray],
    threshold: int,
) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
    h, w = images[0].shape[:2]
    combined_alpha = np.zeros((h, w), dtype=np.uint8)

    for img in images:
        alpha = img[:, :, 3]
        combined_alpha = np.maximum(combined_alpha, alpha)

    mask = combined_alpha > threshold
    if not np.any(mask):
        return None, None, None, None

    rows, cols = np.where(mask)
    left = int(cols.min())
    right = int(cols.max())
    top = int(rows.min())
    bottom = int(rows.max())

    return left, right, top, bottom


def crop_images_aspect_ratio(
    images: List[np.ndarray],
    global_box: Tuple[int, int, int, int],
    aspect_w: int = 1,
    aspect_h: int = 1,
    margin_percent: float = 0.20,
) -> List[np.ndarray]:
    left, right, top, bottom = global_box

    rect_w = right - left
    rect_h = bottom - top

    if rect_w <= 0 or rect_h <= 0:
        h, w = images[0].shape[:2]
        rect_w = w
        rect_h = h
        left, right, top, bottom = 0, w, 0, h

    aspect_h = max(1, aspect_h)
    aspect_w = max(1, aspect_w)
    aspect_ratio = aspect_w / aspect_h

    base = rect_w if rect_w >= rect_h else rect_h
    margin = int(base * margin_percent)

    if rect_w / rect_h > aspect_ratio:
        crop_w = rect_w + 2 * margin
        crop_h = int(crop_w / aspect_ratio)
    else:
        crop_h = rect_h + 2 * margin
        crop_w = int(crop_h * aspect_ratio)

    cx = (left + right) // 2
    cy = (top + bottom) // 2

    half_w = crop_w // 2
    half_h = crop_h // 2

    crop_left = cx - half_w
    crop_right = cx + half_w
    crop_top = cy - half_h
    crop_bottom = cy + half_h

    white_bg = np.ones((crop_h, crop_w, 3), dtype=np.uint8) * 255
    canvas = np.ones((crop_h, crop_w, 4), dtype=np.uint8) * 255

    outputs: List[np.ndarray] = []
    for img in images:
        h, w = img.shape[:2]
        canvas[:, :, :] = 255

        src_x1 = max(0, crop_left)
        src_y1 = max(0, crop_top)
        src_x2 = min(w, crop_right)
        src_y2 = min(h, crop_bottom)

        dst_x1 = src_x1 - crop_left
        dst_y1 = src_y1 - crop_top
        dst_x2 = dst_x1 + (src_x2 - src_x1)
        dst_y2 = dst_y1 + (src_y2 - src_y1)

        if src_x1 < src_x2 and src_y1 < src_y2:
            canvas[dst_y1:dst_y2, dst_x1:dst_x2] = img[
                src_y1:src_y2, src_x1:src_x2
            ]

        alpha = canvas[:, :, 3:4].astype(np.float32) / 255.0
        result = (
            canvas[:, :, :3].astype(np.float32) * alpha
            + white_bg.astype(np.float32) * (1 - alpha)
        )
        outputs.append(result.astype(np.uint8))

    return outputs


def _load_image_entry(path: str) -> Optional[ImageEntry]:
    cv_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    pixmap = QPixmap(path)

    if cv_image is None and pixmap.isNull():
        return None

    if cv_image is None:
        cv_image = _qimage_to_bgra(pixmap.toImage())
    else:
        cv_image = _ensure_bgra(cv_image)

    if pixmap.isNull():
        pixmap = pixmap_from_bgr(cv_image)

    return ImageEntry(path=path, pixmap=pixmap, cv_image=cv_image)


def _ensure_bgra(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
    if image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    if image.shape[2] == 4:
        return image
    raise ValueError("Unsupported image format for conversion.")


def _qimage_to_bgra(image: QImage) -> np.ndarray:
    rgba = image.convertToFormat(QImage.Format_RGBA8888)
    width = rgba.width()
    height = rgba.height()
    ptr = rgba.bits()
    ptr.setsize(rgba.byteCount())
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4)).copy()
    return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
