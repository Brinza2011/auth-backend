from fastapi import APIRouter

users_router = APIRouter()


# @users_router.get("/user", dependencies = [Depends(auth_required)])
# async def get_users(service: UserService = Depends(get_user_svc)):
#     users = await service.get_users()

#     return [
#         {
#             "id": user.id,
#             "name": user.username,
#             "email": user.email
#         }
#         for user in users
#     ]
