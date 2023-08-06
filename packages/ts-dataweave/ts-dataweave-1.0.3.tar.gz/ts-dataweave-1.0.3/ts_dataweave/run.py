import os
import re
import subprocess
import sys
import json

from io import BufferedIOBase
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Union

from .as_bytes import as_bytes
from .Error import Error
from .Payload import Payload

def run(payload: Dict[str, Payload], script: Union[str, bytes, BufferedIOBase], timeout=30) -> bytes:
    """Executes DataWeave with the specified payloads and script.

    Args:
        payload (Dict[str, Payload]): Dictionary of payloads to pass
            to the DataWeave script. Payloads will be written to temporary
            files and then removed after execution.
        script (Union[str, bytes, BufferedIOBase]): DataWeave script. Will be
            written to a temporary file and removed after execution.
        timeout (int, optional): Timeout in seconds for script execution.
            Defaults to 30.

    Returns:
        bytes: Output from the DataWeave script.
    """

    args = [ str((Path(__file__) / ".." / "bin" / "dw").resolve()) ]

    # convert payloads to temp files
    for p in iter(payload):
        payload_id = re.sub(r"\W+", "_", p)
        with NamedTemporaryFile("wb", suffix=f"-{payload_id}.{payload[p].payloadType}", delete=False) as temp_file:
            temp_file.write(payload[p].data)
            payload[p].data = temp_file.name
        args.append("--input")
        args.append(payload_id)
        args.append(payload[p].data)

    # convert script file to temp file
    with NamedTemporaryFile("wb", suffix="-script.dwl", delete=False) as temp_file:
        temp_file.write(as_bytes(script))
        script = temp_file.name
    args.append("--file")
    args.append(script)

    # direct output to file
    with NamedTemporaryFile("wb", suffix="-output", delete=False) as temp_file:
        output_filename = temp_file.name
    args.append("--output")
    args.append(output_filename)

    try:

        # execute dataweave
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            timeout=timeout
        )

        # open the output file
        try:
            with open(output_filename, "rb") as fh:
                out_bytes = fh.read()
        except:
            out_bytes = None

        # do we have any output data?
        if out_bytes is None or len(out_bytes) == 0:
            raise Error(
                "DataWeave execution failed.",
                executable=args[0],
                parameters=args[1:],
                stdout=result.stdout.decode("utf-8"),
                stderr=result.stderr.decode("utf-8")
            )

    # propagate DataWeave errors instead of wrapping
    except Error as e:
        raise e

    # catch any system-level errors
    except Exception as e:
        raise Error(
            "DataWeave execution failed: " + str(e),
            executable=args[0],
            parameters=args[1:],
            stdout="",
            stderr=e.args
        )

    # clean up temporary files
    finally:
        
        # remove temporary files
        for p in iter(payload):
            os.remove(payload[p].data)
        os.remove(script)
        os.remove(output_filename)

    return out_bytes

    