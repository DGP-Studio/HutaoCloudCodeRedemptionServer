from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
import redemption

router = APIRouter(prefix="/management", tags=["management"])


@router.post("/add")
async def add_code_to_db(request: Request):
    # Handle Parameters
    request = await request.json()
    number_of_code = int(request.get("n"))
    value = request.get("v")
    description = request.get("desc")
    added_by = request.get("author")

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
async def get_all_unused_code():
    result = redemption.get_all_unused_redemption_code()
    file_name = redemption.generate_redemption_code_list_txt(result)
    return FileResponse(path=file_name, filename="generated_codes.txt", media_type="text/plain")
