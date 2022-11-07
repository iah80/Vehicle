

class Violation:
    def __init__(self):
        self.__time: str = ""
        self.__link_video: str = ""
        self.__plate: str = ""
        self.__speed: float = 0.0

    def getTime(self) -> str:
        return self.__time

    def getLinkVideo(self) -> str:
        return self.__link_video

    def getPlate(self) -> str:
        return self.__plate

    def getSpeed(self) -> float:
        return self.__speed

    def setTime(self, time: str):
        self.__time = time

    def setLinkVideo(self, link_video: str):
        self.__link_video = link_video

    def setPlate(self, plate: str):
        self.__plate = plate

    def setSpeed(self, speed: float):
        self.__speed = speed
