"""Сервис перевода."""

from deep_translator import GoogleTranslator


class TranslatorService:
    """Сервис для перевода текста."""

    def __init__(self):
        self._cache = {}

    def translate(self, text: str, source: str, target: str) -> str:
        """
        Перевести текст.

        Args:
            text: Исходный текст
            source: Исходный язык ('auto' для автоопределения)
            target: Целевой язык

        Returns:
            Переведенный текст
        """
        # Проверяем кэш
        cache_key = (text, source, target)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Переводим
        translator = GoogleTranslator(source=source, target=target)
        result = translator.translate(text)

        # Сохраняем в кэш
        self._cache[cache_key] = result

        # Ограничиваем размер кэша
        if len(self._cache) > 100:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

        return result