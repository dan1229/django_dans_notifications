import json

from django.test import TestCase
from drf_yasg import openapi
from drf_yasg.codecs import OpenAPICodecJson
from drf_yasg.generators import OpenAPISchemaGenerator

from ...urls import urlpatterns


"""
# =============================================================================================
# SWAGGER SCHEMA GENERATION TESTS =============================================================
# =============================================================================================
"""


class SwaggerSchemaGenerationTestCase(TestCase):
    """
    Regression test for the `list` endpoints' hand-built paginated response schema.

    A raw serializer instance nested inside a manually constructed `openapi.Schema` tree
    (rather than passed as the top-level `responses=` value) does not get auto-resolved by
    drf-yasg, and instead survives into the final document as a live serializer object,
    which blows up `json.dumps()` with "Object of type <Serializer> is not JSON serializable".
    This only surfaces when the schema is actually encoded (e.g. `?format=openapi`), not when
    it's merely generated, so both steps are required to catch a regression.
    """

    def test_schema_generation_and_json_encoding(self) -> None:
        generator = OpenAPISchemaGenerator(
            info=openapi.Info(title="Test", default_version="v1"),
            patterns=urlpatterns,
        )
        schema = generator.get_schema(request=None, public=True)
        codec = OpenAPICodecJson(validators=[])

        # `encode()` IS the assertion. It runs one `json.dumps()` over the whole
        # merged document, so a leaked serializer instance in any one of the three
        # viewsets raises here. Do not "tighten" this into a try/except.
        encoded = codec.encode(schema)

        # Each list response must resolve to a named definition rather than a raw
        # serializer - this is what regressed. Checking the paths alone would not
        # catch a dropped response schema.
        document = json.loads(encoded)
        for path, tag in (
            ("/basic/", "PaginatedNotificationBasic"),
            ("/email/", "PaginatedNotificationEmail"),
            ("/push/", "PaginatedNotificationPush"),
        ):
            self.assertIn(path, document["paths"])
            list_200 = document["paths"][path]["get"]["responses"]["200"]
            self.assertEqual(list_200["schema"]["$ref"], f"#/definitions/{tag}")
            self.assertIn(tag, document["definitions"])
