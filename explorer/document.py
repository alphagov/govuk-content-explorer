class Document(object):
    """A document returned from elasticsearch.

    This class mainly exists to force the returned fields into consistent
    representations; fields which can only have at most one value are coerced
    into strings (or None).  Other fields which may have an arbitrary number of
    values are coerced into lists (even if elasticsearch returns them as a
    single string when they're single-valued).

    """
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
        return self._tuplefield(fieldname)
