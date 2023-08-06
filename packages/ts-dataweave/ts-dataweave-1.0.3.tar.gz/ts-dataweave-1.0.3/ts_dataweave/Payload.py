from functools import singledispatch
from io import BufferedIOBase
from json import dumps
from typing import Union

from .as_bytes import as_bytes
from .PayloadType import PayloadType

class Payload:
    """Creates a new DataWeave payload instance.

    Args:
        payloadType (PayloadType): payload content type (default = JSON)
        data (Union[str, bytes, dict, list, BufferedIOBase]): payload data as string, bytes, or file-like object
    """

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (str, bytes, dict, list, BufferedIOBase)):

            # save the data
            self.data = as_bytes(args[0])

            # if data is `dict` or `list`, treat it like JSON
            if isinstance(args[0], (dict, list)):
                self.payloadType = PayloadType.JSON

            # try to detect data type
            else:

                # get first byte of the data
                first_nonwhitespace_byte = self.data.strip()[0]
                print("first byte =", first_nonwhitespace_byte)

                # JSON starts with `{` or `[`
                if first_nonwhitespace_byte == b"{"[0] \
                    or first_nonwhitespace_byte == b"["[0]:
                    self.payloadType = PayloadType.JSON

                # XML starts with `<`
                elif first_nonwhitespace_byte == b"<"[0]:
                    self.payloadType = PayloadType.XML

                # hopefully it's CSV
                else:
                    self.payloadType = PayloadType.CSV

        # if 2 args, then first arg is payload type, second is data
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[0], (str, bytes, dict, list, BufferedIOBase)):
            self.payloadType = args[0]
            self.data = as_bytes(args[1])

        # raise error if we don't have the expected args
        else:
            raise Exception(f"Expected 1 or 2 args, got {len(args)}.")

