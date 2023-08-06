from fastapi.exceptions import HTTPException

class Permission:

    """
    r -> read -> 4 = GET
    w -> write -> 2 = PUT
    d -> delete -> 1 = DELETE

    0 = ---
    1 = --d
    2 = -w-
    3 = -wd
    4 = r--
    5 = r-d
    6 = rw-
    7 = rwd
    """

    def __init__(self, operation, user_uuid, resource):
        self.operation = operation
        self.user_uuid = user_uuid
        self.resource = resource

    async def _get_perms(operation, perms, index):

        operation = int(operation)
        perms_for_user = int(str(perms)[index])

        if operation == 4 and perms_for_user in [4,5,6,7]:
            return True

        elif operation == 2 and perms_for_user in [2,3,6,7]:
            return True

        elif operation == 1 and perms_for_user in [1,3,5,7]:
            return True

        else:
            raise HTTPException(403)


    async def _is_allowed(self, 
        operation = 0, 
        perms = 000, 
        user_uuid = None, 
        owner = None, 
        group = []):

        if  user_uuid == owner:
            return await self._get_perms(operation , perms, 0)

        elif user_uuid in group:
            return await self._get_perms(operation , perms, 1)

        elif user_uuid not in group:
            return await self._get_perms(operation , perms, 2)


    async def get_verdict(self):

        if isinstance(self.operation, str):
            http_perms_key = {
                "GET": 4,
                "PUT": 2,
                "DELETE": 1
            }
            self.operation = http_perms_key[self.operation]
            
        return await self._is_allowed(self.operation, self.resource.permissions, self.user_uuid, self.resource.owner, self.resource.group)
