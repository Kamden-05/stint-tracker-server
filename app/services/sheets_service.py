from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import settings
from app.logger import get_logger
from app.models import Base
from typing import List
logger = get_logger(__name__)


def update_range(sheet_id: str, range_name: str, models: List[Base]) -> None:

    creds = service_account.Credentials.from_service_account_file(
        settings.SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    try:
        service = build("sheets", "v4", credentials=creds)
        
        values = [list(col.name for col in models[0].__table__.columns)]
        for model in models:
            values.append(list(getattr(model, col.name) for col in models[0].__table__.columns))
            
        body = {"values": values}

        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )

        logger.info(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as e:
        logger.error(f"An error occurred: {str(e)}")
        return e
