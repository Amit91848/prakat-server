from models.Admin import Admin


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin
