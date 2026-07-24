"""
============================================================
EduMindAI Enterprise v3.0
Internet Search Engine
============================================================
"""

from duckduckgo_search import DDGS

from config import ENABLE_WEB_SEARCH


class SearchEngine:

    def __init__(self):

        self.enabled = ENABLE_WEB_SEARCH

    # =====================================================
    # ENABLE
    # =====================================================

    def enable(self):

        self.enabled = True

    # =====================================================

    def disable(self):

        self.enabled = False

    # =====================================================

    def is_enabled(self):

        return self.enabled
        # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query,
        max_results=5
    ):

        if not self.enabled:
            return []

        try:

            with DDGS() as ddgs:

                results = list(

                    ddgs.text(
                        keywords=query,
                        max_results=max_results
                    )

                )

                return results

        except Exception:

            return []

    # =====================================================
    # CONTEXT
    # =====================================================

    def search_context(
        self,
        query,
        max_results=5
    ):

        results = self.search(
            query,
            max_results
        )

        if not results:

            return ""

        context = ""

        for index, item in enumerate(results, start=1):

            title = item.get("title", "")

            body = item.get("body", "")

            href = item.get("href", "")

            context += (
                f"{index}. {title}\n"
                f"{body}\n"
                f"Manba: {href}\n\n"
            )

        return context
        # =====================================================
    # SIMPLE SEARCH
    # =====================================================

    def ask(
        self,
        query
    ):

        return self.search_context(query)

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.enabled = ENABLE_WEB_SEARCH


# =====================================================
# SEARCH OBJECT
# =====================================================

search = SearchEngine()

