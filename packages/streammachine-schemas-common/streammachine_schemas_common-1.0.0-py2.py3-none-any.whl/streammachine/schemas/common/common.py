from abc import ABC, abstractmethod


class StreamMachineEvent(ABC):
    @abstractmethod
    def get_strm_schema_ref(self) -> str:
        pass

    def get_strm_schema_id(self) -> str:
        return self.get_strm_schema_ref

    @abstractmethod
    def get_strm_schema(self):
        pass

    @abstractmethod
    def get_strm_schema_type(self):
        pass
