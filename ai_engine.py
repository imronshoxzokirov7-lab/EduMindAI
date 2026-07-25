# =====================================================
    # IMAGE GENERATION
    # =====================================================

    def generate_image(self, prompt: str):
        """
        Matnli tasvir orqali AI yordamida rasm yaratish.
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                response_format="url"
            )
            return response.data[0].url
        except Exception:
            try:
                # Muqobil bepul model
                response = self.client.images.generate(
                    model="flux",
                    prompt=prompt,
                    response_format="url"
                )
                return response.data[0].url
            except Exception:
                return None
