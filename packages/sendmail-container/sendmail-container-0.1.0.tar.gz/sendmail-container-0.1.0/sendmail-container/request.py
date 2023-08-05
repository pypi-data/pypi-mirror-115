from pathlib import Path
from typing import List, Optional, Tuple, Union

import requests
from pydantic import AnyUrl, BaseModel, validator


class FormDataRequest(BaseModel):
    attachments: Optional[List[Path]] = None
    sender_prefix: Optional[str] = None
    recipients: Union[str, List]
    mail_title: Optional[str] = None
    mail_body: Optional[str] = None

    request_uri: AnyUrl

    @validator("recipients")
    def recipients_as_list(cls, value) -> List:
        if isinstance(value, str):
            return value.split(",")
        return value

    def get_multipart_form(self) -> Tuple:
        form_data_dict = self.dict(exclude_none=True)
        multipart_list = []
        for key, value in form_data_dict.items():
            if key == "attachments":
                for v in value:
                    multipart_list.append((key, (Path(v).name, open(v))))
            elif isinstance(value, list):
                for v in value:
                    multipart_list.append((key, (None, v)))
            elif isinstance(value, str):
                multipart_list.append((key, (None, value)))
        return tuple(multipart_list)

    def submit(self) -> requests.Response:
        return requests.post(url=str(self.request_uri), files=self.get_multipart_form())
