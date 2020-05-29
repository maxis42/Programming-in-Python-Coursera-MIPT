from abc import ABC, abstractmethod


# class Engine:
#     pass


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, achievement):
        for subscriber in self.__subscribers:
            subscriber.update(achievement)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, achievement):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []

    def update(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
