from dataclasses import dataclass

from backend.src.infrastructure.nlp.mws_gpt_test import MWSGptForTest
from backend.src.config import settings


@dataclass
class AppContext:
    mws_gpt: MWSGptForTest


def get_app_context():
    return AppContext(
        mws_gpt=MWSGptForTest(),
    )


context = get_app_context()
