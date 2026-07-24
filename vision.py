"""
============================================================
EduMindAI Enterprise v3.0
Vision Manager
============================================================
"""

from PIL import Image


class VisionManager:

    def __init__(self):

        pass

    # =====================================================
    # OPEN IMAGE
    # =====================================================

    def open(
        self,
        file
    ):

        try:

            image = Image.open(file)

            return image.convert("RGB")

        except Exception:

            return None

    # =====================================================
    # IMAGE INFO
    # =====================================================

    def info(
        self,
        image
    ):

        if image is None:

            return {}

        return {

            "width": image.width,

            "height": image.height,

            "size": image.size,

            "mode": image.mode,

            "format": image.format

        }
        # =====================================================
    # RESIZE IMAGE
    # =====================================================

    def resize(
        self,
        image,
        width=1024,
        height=1024
    ):

        if image is None:

            return None

        return image.resize((width, height))

    # =====================================================
    # THUMBNAIL
    # =====================================================

    def thumbnail(
        self,
        image,
        size=(300, 300)
    ):

        if image is None:

            return None

        img = image.copy()

        img.thumbnail(size)

        return img

    # =====================================================
    # SAVE IMAGE
    # =====================================================

    def save(
        self,
        image,
        path
    ):

        if image is None:

            return False

        try:

            image.save(path)

            return True

        except Exception:

            return False
            # =====================================================
    # VALIDATE IMAGE
    # =====================================================

    def is_valid(
        self,
        image
    ):

        return image is not None

    # =====================================================
    # IMAGE DESCRIPTION
    # =====================================================

    def description(
        self,
        image
    ):

        if image is None:

            return "Rasm topilmadi."

        info = self.info(image)

        return (
            f"Rasm hajmi: {info['width']}x{info['height']}\n"
            f"Rang rejimi: {info['mode']}"
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        pass


# =====================================================
# VISION OBJECT
# =====================================================

vision = VisionManager()

