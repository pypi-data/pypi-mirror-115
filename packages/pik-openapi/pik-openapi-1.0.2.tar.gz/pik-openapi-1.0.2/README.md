## PIK OPENAPI Tools

Some PIK protocol DRF openapi extensions:
  - inspection
    - Schema version fetching from `RELEASE` env variable.
    - Schema title generation as `f'{settings.SERVICE_TITLE} API'`.
    - Components schemas generation from ModelSerializers.
    - Schema description fetching from `settings.SERVICE_DESCRIPTION`
    - `SerializerMethodField` type hint introspection.
    - type field `enum`
    - model introspection:
      -`label` as `title`
      - `help_text` as `description` 
      - `label` as `x-title-plural`
    - correct `ListField` item typing
    - choice labels as `x-enumNames`
    - deprecated fields marking
    - `NullBooleanField` type fix
    - Type hints for `SerializerMethodField`
    - `JSONField` schema
    - inspect filters for list endpoint only
    - Schema customization with `update_schema` property or method
    - Operation labels & description
    - RESTQL parameter schema
  - etc
    - Automatic camelCase translation
      - schema
      - filters
      - params
      - restql
    - PIK OpenID Schema
  - renderers
    - CachedRenderer mixin - returns pre-rendenred file if exists:
        - replaces "/" with "_" to get filename
        - `/api/v1/schema/` searches `{STATIC_ROOT}/_api_v1_schema_.html`
        - `/api/v1/schema/?format=openapi` searches `{STATIC_ROOT}/_api_v1_schema_.yaml`
        - `/api/v1/schema/?format=openapi.json` searches `{STATIC_ROOT}/_api_v1_schema_.json`
    - JSONOpenPrettyRenderer
    - RedocOpenAPIRenderer
  - generateopenapi management command

## Installation

- Add `pik_openapi` to `INSTALLED_APPS` in `settings.py`
```python
INSTALLED_APPS = [
    ...
    'pik_openapi',
]
```

- Setup default schema inspector class with `settings.py`
```python
REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'core.api.openapi.openapi.PIKAutoSchema',
  ...
}
```

- Setup schema url with `urls.py`
```python
from core.api.openapi.views import get_pik_schema_view

router_api_v1 = DefaultRouter()
api_v1_path = [path(
    'api/v1/', include((router_api_v1.urls, 'api_v1')))]

urlpatterns = [
    *api_v1_path,
    
    path('api/v1/schema/',
         get_pik_schema_view(
             title=f'API Schema',
             patterns=api_v1_path),
         name='api_v1_schema'),]
```

## Usage

- Redoc schema is available at /api/v1/schema/ and /api/v1/schema/?format=redoc
- Json schema format available at /api/v1/schema/?format=openapi-json
- YAML schema format available at /api/v1/schema/?format=openapi
- Generate pre-rendered json schema file:
```sh  
  ./manage.py generateopenapi \
    --format=openapi-json \
  --urlpatterns=_project_.urls.api_v1_path \
  > ${STATIC_ROOT}/_api_v1_schema_.json
```
- Generate pre-rendered openapi schema file:
```sh  
  ./manage.py generateopenapi \
    --format=openapi \
  --urlpatterns=_project_.urls.api_v1_path \
  > ${STATIC_ROOT}/_api_v1_schema_.yaml
```
- Generate redoc bundle with [redoc-cli](https://www.npmjs.com/package/redoc-cli#user-content-usage)
```bash
  redoc-cli bundle 
  ${STATIC_ROOT}/_api_v1_schema_.json \
  --output ${STATIC_ROOT}/_api_v1_schema_.html \
  --options.showExtensions=true
```

## Features


### Schema Customization


#### Serializer schema customization

Inject schema customization, through `update_schema` dict:

```python
class MySerializer(ModelSerializer):
    update_schema = {
        'properties': {
            'uid': {'deprecated': True}
        }
    }
```

Inject schema customization, though `update_schema` callback:

```python
class MySerializer(ModelSerializer):
    def update_schema(self, schema):
        schema['properties']['_uid']['deprecated'] = True
        return schema
```

#### ViewSet Schema customization

Inject schema customization, through `update_schema` dict:

```python
class MyViewSet(ViewSet):
    update_schema = {
        '/api/v1/comment-list/': {
            'get': {
                'deprecated': True,
            }
        }
    }
```
Inject schema customization, though `update_schema` callback:

```python
class MyViewSet(ViewSet):
    def update_schema(self, schema):
        schema['/api/v1/comment-list/']['get']['deprecated'] = True
        return schema
```

### Generate Schema as HTML File
------------------------

For generate schema as HTML file:

- Install [redoc-cli](https://github.com/Redocly/redoc/blob/master/cli/README.md)
```bash
npm install -g redoc-cli
```
- Get your schema file
- Generate HTML file with `redoc-cli`
```bash
redoc-cli bundle static/_api_v1_schema_.json \
--output static/_api_v1_schema_.html
```

More info ``
