from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class SlugPrefixRouter(SimpleRouter):
    """
    Custom router for APIs that include a dynamic slug in the URL structure.

    This router allows defining API endpoints with a `{slug}` segment, making it
    useful for resources that need slug-based identification (e.g., organizations, 
    categories, or user-specific routing).

    ## URL Structure:
    - `{slug}/{prefix}/` → List and Create operations (`GET` & `POST`)
    - `{slug}/{prefix}/{lookup}/` → Retrieve, Update, and Delete operations (`GET`, `PUT`, `PATCH`, `DELETE`)
    - `{slug}/{prefix}/{url_path}/` → Dynamic actions based on viewset methods (`GET`)

    ## Route Definitions:
    
    1. **List & Create (`list`, `create`)**
       - URL pattern: `^{slug}/{prefix}{trailing_slash}$`
       - Maps:
         - `GET`: List view (retrieve all items)
         - `POST`: Create a new item
       - Example usage:
         ```
         GET /company-abc/products/
         POST /company-abc/products/
         ```

    2. **Detail (`retrieve`, `update`, `partial_update`, `destroy`)**
       - URL pattern: `^{slug}/{prefix}/{lookup}{trailing_slash}$`
       - Maps:
         - `GET`: Retrieve a specific item
         - `PUT` / `PATCH`: Update item
         - `DELETE`: Delete item
       - Example usage:
         ```
         GET /company-abc/products/42/
         DELETE /company-abc/products/42/
         ```

    3. **Dynamic Routes (`detail=True`)**
       - URL pattern: `^{slug}/{prefix}/{url_path}{trailing_slash}$`
       - Handles dynamic viewset actions (`@action`)
       - Example usage:
         ```
         GET /company-abc/products/42/activate/
         ```
    """
    routes = [
        Route(
            url=r"^{slug}/{prefix}{trailing_slash}$",
            mapping={
                'get': 'list',
                'post': 'create',
            },
            name="{basename}-list",
            detail=True,
            initkwargs={'suffix': 'List'},        
        ),
        Route(
            url=r"^{slug}/{prefix}/{lookup}{trailing_slash}$",
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={'suffix': 'Instance'},
        ),
        DynamicRoute(
            url=r'^{slug}/{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]