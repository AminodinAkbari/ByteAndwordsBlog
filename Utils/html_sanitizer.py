"""This file includes classes for html content cleaner for security masures (sanitizing.)"""
import bleach


class PostHtmlContentSanitizer:

    def __init__(self):
        self.ALLOWED_TAGS = [
            "p", "br", "hr",
            "strong", "em", "u", "s", "blockquote", "code", "pre",
            "ul", "ol", "li",
            "h1", "h2", "h3", "h4",
            "a", "img", "table", "thead", "tbody", "tr", "th", "td",
        ]
        self.ALLOWED_ATTRS = {
            "a": ["href", "title"],
            "img": ["src", "alt", "title"],
            "th": ["colspan", "rowspan"],
            "td": ["colspan", "rowspan"],
        }
        self.ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


    def sanitize_html(self , html_content: str) -> str:
        """
        Returns a sanitized HTML string:
        - strips disallowed tags/attrs
        - blocks javascript/data URLs
        - removes event handlers (onclick, etc.)
        """
        if not html_content:
            return ""

        cleaned = bleach.clean(
            html_content,
            tags = self.ALLOWED_TAGS,
            attributes = self.ALLOWED_ATTRS,
            protocols = self.ALLOWED_PROTOCOLS,
            strip= True, # drop disallowed tags entirely
            strip_comments = True
        )

        hardened = bleach.linkify(
            cleaned,
            callbacks=[self.set_rel],
            skip_tags=["pre" , "code"], # Don't touch code blocks.
            parse_email = True
        )

        return hardened

    def set_rel(self, attrs, new=False):
        """
        Callback for bleach.linkify that hardens <a> tags.
        Always adds rel="nofollow noopener noreferrer" and target="_blank".
        """
        href = attrs.get("href", "")
        if href:
            # Always harden rel on anchors
            attrs["rel"] = "nofollow noopener noreferrer"
            attrs["target"] = "_blank"
        return attrs
