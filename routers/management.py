from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import FileResponse
import redemption
import authorization

router = APIRouter(prefix="/management", tags=["management"])


@router.post("/add")
async def add_code_to_db(request: Request) -> FileResponse:
    # Validate Token
    token = request.headers.get("Authorization")
    is_admin_result, added_by = authorization.is_admin(token)
    if not is_admin_result:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Handle Parameters
    request = await request.json()
    number_of_code = int(request.get("n"))
    value = request.get("v")
    description = request.get("desc")

    # Process to add codes
    number_of_success = 0
    added_codes = []
    while number_of_success < number_of_code:
        code = redemption.generate_redemption_code()
        if redemption.add_redemption_code_to_database(code, value, description, added_by):
            number_of_success += 1
            added_codes.append(code)
    file_name = redemption.generate_redemption_code_list_txt(added_codes)
    return FileResponse(path=file_name, filename="generated_codes.txt", media_type="text/plain")


@router.get("/get_all_unused", tags=["management"])
async def get_all_unused_code(request: Request) -> FileResponse:
    # Validate Token
    token = request.headers.get("Authorization")
    if not authorization.is_admin(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = redemption.get_all_unused_redemption_code()
    file_name = redemption.generate_redemption_code_list_txt(result)
    return FileResponse(path=file_name, filename="generated_codes.txt", media_type="text/plain")
