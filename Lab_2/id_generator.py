class IDGenerator:
    """Генератор унікальних ID для всіх об'єктів симуляції."""
    _current_id = 0

    @classmethod
    def get_next_id(cls):
        """Повертає наступний унікальний ID і збільшує лічильник."""
        cls._current_id += 1
        return cls._current_id

    @classmethod
    def reset(cls):
        """Скидає лічильник ID (для тестування)."""
        cls._current_id = 0