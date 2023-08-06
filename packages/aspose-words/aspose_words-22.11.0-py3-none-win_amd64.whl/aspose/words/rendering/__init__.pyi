﻿import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class NodeRendererBase:
    '''Base class for :class:`ShapeRenderer` and :class:`OfficeMathRenderer`.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/net/working-with-shapes/>` documentation article.'''
    
    @overload
    def save(self, file_name: str, save_options: aspose.words.saving.ImageSaveOptions) -> None:
        '''Renders the shape into an image and saves into a file.
        
        :param file_name: The name for the image file. If a file with the specified name already exists, the existing file is overwritten.
        :param save_options: Specifies the options that control how the shape is rendered and saved. Can be ``None``.'''
        ...
    
    @overload
    def save(self, stream: io.BytesIO, save_options: aspose.words.saving.ImageSaveOptions) -> None:
        '''Renders the shape into an image and saves into a stream.
        
        :param stream: The stream where to save the image of the shape.
        :param save_options: Specifies the options that control how the shape is rendered and saved. Can be ``None``.
                             If this is ``None``, the image will be saved in the PNG format.'''
        ...
    
    ...

class OfficeMathRenderer(aspose.words.rendering.NodeRendererBase):
    '''Provides methods to render an individual :class:`aspose.words.math.OfficeMath`
    to a raster or vector image or to a Graphics object.
    To learn more, visit the `Working with OfficeMath <https://docs.aspose.com/words/net/working-with-officemath/>` documentation article.'''
    
    def __init__(self, math: aspose.words.math.OfficeMath):
        '''Initializes a new instance of this class.
        
        :param math: The :class:`aspose.words.math.OfficeMath` object that you want to render.'''
        ...
    
    ...

class PageInfo:
    '''Represents information about a particular document page.
    To learn more, visit the `Rendering <https://docs.aspose.com/words/net/rendering/>` documentation article.
    
    The page width and height returned by this object represent the "final" size of the page e.g. they are
    already rotated to the correct orientation.'''
    
    @property
    def paper_size(self) -> aspose.words.PaperSize:
        '''Gets the paper size as enumeration.'''
        ...
    
    @property
    def width_in_points(self) -> float:
        '''Gets the width of the page in points.'''
        ...
    
    @property
    def height_in_points(self) -> float:
        '''Gets the height of the page in points.'''
        ...
    
    @property
    def paper_tray(self) -> int:
        '''Gets the paper tray (bin) for this page as specified in the document.
        The value is implementation (printer) specific.'''
        ...
    
    @property
    def landscape(self) -> bool:
        '''Returns ``True`` if the page orientation specified in the document for this page is landscape.'''
        ...
    
    ...

class ShapeRenderer(aspose.words.rendering.NodeRendererBase):
    '''Provides methods to render an individual :class:`aspose.words.drawing.Shape` or :class:`aspose.words.drawing.GroupShape`
    to a raster or vector image or to a Graphics object.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/net/working-with-shapes/>` documentation article.'''
    
    def __init__(self, shape: aspose.words.drawing.ShapeBase):
        '''Initializes a new instance of this class.
        
        :param shape: The DrawinML shape object that you want to render.'''
        ...
    
    ...

class ThumbnailGeneratingOptions:
    '''Can be used to specify additional options when generating thumbnail for a document.
    
    User can call method :meth:`aspose.words.Document.update_thumbnail` to generate
    :attr:`aspose.words.properties.BuiltInDocumentProperties.thumbnail` for a document.'''
    
    def __init__(self):
        ...
    
    @property
    def generate_from_first_page(self) -> bool:
        '''Specifies whether to generate thumbnail from first page of the document or first image.
        
        Default is ``True``, which means thumbnail will be generated from first page of the document.
        If value is ``False`` and there is no image in the document, thumbnail will be generated
        from first page of the document.'''
        ...
    
    @generate_from_first_page.setter
    def generate_from_first_page(self, value: bool):
        ...
    
    ...

