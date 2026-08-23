from fastapi import APIRouter, status, Response

router = APIRouter(
  prefix="/health",
  tags=["Healthcheck"],
)


@router.get(
  path="/health/",
  status_code=status.HTTP_200_OK,
  response_class=Response,
  responses={
      status.HTTP_200_OK: {"description": "Healthy"},
  }
)
async def health():
    return Response(status.HTTP_200_OK)