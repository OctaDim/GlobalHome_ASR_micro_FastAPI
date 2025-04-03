# import httpx
# from fastapi import HTTPException
#
#
# async def make_request(url: str, data: dict):
#     headers = {"Content-Type": "application/json"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=data, headers=headers)
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail=response.json())
#         return response.json()
