import dateutil.parser

class Document(object):
    """A document returned from elasticsearch.

    This class mainly exists to force the returned fields into consistent
    representations; fields which can only have at most one value are coerced
    into strings (or None).  Other fields which may have an arbitrary number of
    values are coerced into lists (even if elasticsearch returns them as a
    single string when they're single-valued).

    """

    # The fields that we want to be able to display on documents.
    DISPLAY_FIELDS = (
        "title",
        "link",
        "slug",
        "document_collections",
        "display_type",
        "description",
        "specialist_sectors",
        "mainstream_browse_pages",
        "organisations",
        "format",
        "public_timestamp",
    )

    # Fields that we want to facet on
    FACET_FIELDS = (
        "document_collections",
        "specialist_sectors",
        "mainstream_browse_pages",
        "organisations",
        "format",
    )

    def __init__(self, fields):
        self.fields = fields

    def _strfield(self, fieldname):
        val = self.fields.get(fieldname, None)
        if val is None:
            return None
        elif isinstance(val, basestring):
            return val
        else:
            return val[0]

    def _datefield(self, fieldname):
        val = self._strfield(fieldname)
        if val is None:
            return None
        return dateutil.parser.parse(val)

    def _tuplefield(self, fieldname):
        val = self.fields.get(fieldname, ())
        if val is None:
            return ()
        if isinstance(val, basestring):
            return (val,)
        else:
            return tuple(val)

    @property
    def format(self):
        """The format field often has duplicated entries.

        We don't want to display these, so just remove duplicates.  The order
        isn't significant, so we then sort to make it consistent.

        """
        return tuple(sorted(set(self._tuplefield("format"))))

    def __getattr__(self, fieldname):
        if fieldname in (
            "title",
            "link",
            "slug",
            "document_type",
            "index",
            "display_type",
            "description",
        ):
            return self._strfield(fieldname)
        elif fieldname in (
            "public_timestamp",
        ):
            return self._datefield(fieldname)
        return self._tuplefield(fieldname)
