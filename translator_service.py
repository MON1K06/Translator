"""Оптимизированный сервис перевода."""

from deep_translator import GoogleTranslator


class TranslatorService:
    """Синглтон сервиса перевода с кэшированием."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
            cls._instance._translators = {}
        return cls._instance

    def translate(self, text: str, source: str, target: str) -> str:
        """Перевод с кэшированием."""
        # Проверяем кэш
        cache_key = (text[:100], source, target)  # Ограничиваем ключ
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Переиспользуем переводчик
        translator_key = (source, target)
        if translator_key not in self._translators:
            self._translators[translator_key] = GoogleTranslator(
                source=source, target=target
            )

        result = self._translators[translator_key].translate(text)

        # Кэшируем (максимум 50 записей)
        if len(self._cache) >= 50:
            # Удаляем старые
            keys = list(self._cache.keys())[:10]
            for k in keys:
                del self._cache[k]

        self._cache[cache_key] = result
        return result