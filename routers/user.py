from fastapi import HTTPException, Request, APIRouter, Response, status
import homa
import redemption

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/use")
async def use_code_on_user(request: Request, response: Response):
    # Handle Parameters
    request = await request.json()
    code = request.get("code")
    user_name = request.get("user_name")

    if len(code) != 18:
        # Invalid code length
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"status": 403, "message": "Invalid code"}
    if not redemption.validate_redemption_code(code):
        # Code does not exist (whatever status is)
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"status": 403, "message": "Invalid code"}

    func_result = redemption.use_redemption_code(code, user_name)
    if func_result == 0:
        # Code may already be used
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"status": 403, "message": "Invalid code"}
    elif func_result >= 1:
        code_value = redemption.get_code_value(code)
        redeem_result = homa.assign_homa_user_membership_time(user_name, code_value)
        if redeem_result['status'] == 200:
            return redeem_result
        else:
            code_reset_result = redemption.reset_code(code)
            if code_reset_result:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"status": 500, "message": "兑换失败，兑换码未消耗"}
            else:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"status": 500, "message": "兑换失败，请联系管理员"}
