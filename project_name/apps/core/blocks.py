from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock as RichTextBlockBase,
    StreamBlock,
    StructBlock,
    TextBlock,
    PageChooserBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class CaptionedImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    # Remove get_preview_value as it's not supported in this Wagtail version

    class Meta:
        icon = "image"
        template = "blocks/captioned_image_block.html"
        preview_template = "blocks/preview/captioned_image_block.html"
        preview_value = {
            "caption": "Sample image caption",
            "attribution": "Company Name",
        }
        description = "An image with optional caption and attribution"

    def get_preview_context(self, value, parent_context=None):
        return {"value": self.meta.preview_value}


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        preview_template = "blocks/preview/heading_block.html"
        preview_value = {"heading_text": "Section Heading", "size": "h2"}
        description = "A heading with level two, three, or four"

    def get_preview_context(self, value, parent_context=None):
        return {"value": self.meta.preview_value}


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"
        preview_template = "blocks/preview/blockquote.html"
        preview_value = {
            "text": ("A meaningful quote that captures the essence of your message."),
            "attribute_name": "Author Name",
        }
        description = "A quote with an optional attribution"

    def get_preview_context(self, value, parent_context=None):
        return {"value": self.meta.preview_value}


class RichTextBlock(RichTextBlockBase):
    class Meta:
        template = "blocks/rich_text_block.html"
        preview_template = "blocks/preview/paragraph_block.html"
        preview_value = """
            <h2>Our Mission</h2>
            <p>At our company, <b>quality</b> has <i>always</i> been our priority.
            <a href="#">Our products</a> are designed with care and attention to detail.
            We strive to deliver excellence in everything we do.</p>
            """
        description = "A rich text paragraph"

    def get_preview_context(self, value, parent_context=None):
        return {"value": value}


class CustomEmbedBlock(EmbedBlock):
    class Meta:
        help_text = (
            "Insert an embed URL e.g  https://www.youtube.com/watch?v=JGwWNGJdvx8"
        )
        icon = "media"
        template = "blocks/embed_block.html"
        preview_template = "blocks/preview/static_embed_block.html"
        preview_value = {"embed": "https://www.youtube.com/watch?v=XqZsoesa55w"}
        description = "An embedded video or other media"

    def get_preview_context(self, value, parent_context=None):
        return {"value": self.meta.preview_value}


class DocumentDownloadBlock(StructBlock):
    """
    Custom `StructBlock` for document downloads with title and description
    """

    document = DocumentChooserBlock(required=True)
    title = CharBlock(
        required=False,
        help_text="Optional: document title to display instead of the filename",
    )
    description = TextBlock(required=False, help_text="Optional: describe the document")

    class Meta:
        icon = "doc-full"
        template = "blocks/document_download_block.html"
        preview_template = "blocks/preview/document_download_block.html"
        preview_value = {
            "title": "Annual Report 2023",
            "description": "Our comprehensive annual report with financial statements and achievements.",
        }
        description = "A downloadable document with optional title and description"

    def get_preview_context(self, value, parent_context=None):
        return {"value": self.meta.preview_value}


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    rich_text_block = RichTextBlock(
        features=[
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
            "image",
            "embed",
            "code",
            "superscript",
            "subscript",
            "strikethrough",
            "blockquote",
            "ai",
        ]
    )
    image_block = CaptionedImageBlock()
    block_quote = BlockQuote()
    embed_block = CustomEmbedBlock()
    document_block = DocumentDownloadBlock()
    page_link_block = PageChooserBlock()
