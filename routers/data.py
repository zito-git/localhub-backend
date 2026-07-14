from pathlib import Path
import json

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/data",
    tags=["data"],
)

FILES = {
    "tourist": "구미_경북권_관광지.json",
    "leports": "구미_경북권_레포츠.json",
    "culture": "구미_경북권_문화시설.json",
    "shopping": "구미_경북권_쇼핑.json",
    "room": "구미_경북권_숙박.json",
    "course": "구미_경북권_여행코스.json",
    "food": "구미_경북권_음식점.json",
    "event": "구미_경북권_축제공연행사.json",
}


def data_conversion(filename: str):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / filename

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


@router.get(
    "/",
    summary="데이터 API 목록 조회",
    description="사용 가능한 데이터 API 목록을 반환합니다.",
    response_description="사용 가능한 API 목록",
)
def get_data_list():
    return {
        "message": "Available data APIs",
        "apis": [
            {
                "category": key,
                "url": f"/data/{key}",
            }
            for key in FILES
        ],
    }


@router.get(
    "/{category}",
    summary="카테고리 데이터 조회",
    description="""
지원하는 category

- tourist : 관광지
- leports : 레포츠
- culture : 문화시설
- shopping : 쇼핑
- room : 숙박
- course : 여행코스
- food : 음식점
- event : 축제·공연·행사
""",
    response_description="선택한 카테고리의 JSON 데이터",
)
def get_data(category: str):
    filename = FILES.get(category)

    if filename is None:
        raise HTTPException(
            status_code=404,
            detail=f"'{category}'는 지원하지 않는 카테고리입니다.",
        )

    return data_conversion(filename)
