from __future__ import absolute_import

import jpype
import Assist

from strenum import StrEnum


class SaveFormat(StrEnum):
    """!
    Specifies save format
    """

    Pdf = 'Pdf'
    """!
    means saving without change of format, i.e. as PDF use it please instead of
    'SaveFormat.None', that is obsolete one
    """

    Doc = 'Doc'
    """!
    means saving in DOC format
    """

    Xps = 'Xps'
    """!
    means saving in XPS format
    """

    Html = 'Html'
    """!
    means saving in XML format
    """

    Xml = 'Xml'
    """!
    means saving in TEX format i.e. format suitable for Latex text editor
    """

    TeX = 'TeX'
    """!
    means saving in DOCX format
    """

    DocX = 'DocX'
    """!
    means saving in SVG format
    """

    Svg = 'Svg'
    """!
    means saving in SVG format
    """

    MobiXml = 'MobiXml'
    """!
    means saving in MsExcel format
    """

    Excel = 'Excel'
    """!
    means saving in MsExcel format
    """

    Epub = 'Epub'
    """!
    means saving in EPUB format(special format of e-books)
    """


class LoadFormat(StrEnum):
    """!
    Specifies load format
    """

    CGM = 'CGM'
    """!
    means loading of document in CGM format
    """

    HTML = 'HTML'
    """!
    means loading of document in HTML format
    """

    EPUB = 'EPUB'
    """!
    means loading of document in EPUB format(special format of e-books)
    """

    XML = 'XML'
    """!
    means loading of document in XML format(special XML that represent logical structure of PDF document)
    """

    XSLFO = 'XSLFO'
    """!
    means loading of document in XSLFO format
    """

    PCL = 'PCL'
    """!
    means loading of document in PCL format
    """

    XPS = 'XPS'
    """!
    means loading of document in XPS format
    """

    TEX = 'TEX'
    """!
    means loading of document in TEX format - format of Latex text editor
    """

    SVG = 'SVG'
    """!
    means loading of document in SVG format - format of Latex text editor
    """

    MHT = 'MHT'
    """!
    means loading of document in MHT format(that is packed HTML format)
    """

    PS = 'PS'
    """!
    means loading of document in PS format(format of PostScript document) 
    """

    MD = 'MD'
    """!
    means loading document is in MD format (markdown). 
    """

    TXT = 'TXT'
    """!
    means loading document is in TXT format. 
    """

    PDFXML = 'PDFXML'
    """!
    Internal PDF document structure in XML format. 
    """


class Document(Assist.BaseJavaClass):
    """!
    Class representing PDF document
    """

    javaClassName = "com.aspose.python.pdf.Document"

    def __init__(self):
        javaClass = jpype.JClass(Document.javaClassName)
        super().__init__(javaClass)

    def init(self):
        return

    def __init__(self, parameter):

        if parameter is None:
            raise Exception("an argument is required")
        elif parameter.__class__.__name__ == 'bytes':
            javaClass = jpype.JClass(Document.javaClassName)
            super().__init__(javaClass(parameter))
            self.init()
        elif parameter.__class__.__name__ == 'str':
            javaClass = jpype.JClass(Document.javaClassName)
            super().__init__(javaClass(parameter))
            self.init()

    def __init__(self, filename, options):

        if filename is None:
            raise Exception("an argument is required")
        elif filename.__class__.__name__ == 'str':
            javaClass = jpype.JClass(Document.javaClassName)

            if options is None:
                raise Exception("an argument is required")
            elif options.__class__.__name__ == 'LoadOptions':
                super().__init__(javaClass(filename, options.getJClass()))

            self.init()



    def close(self):
        """!
        Closes all resources used by this document.
        """
        self.getJavaClass().close()

    def save(self, fileName, saveFormat):
        """!
        Saves the document with a new name along with a file format.
        """

        SaveFormatClass = "com.aspose.python.pdf.SaveFormat"
        javaClass = jpype.JClass(SaveFormatClass)
        if fileName is None:
            raise Exception("an argument is required")
        elif fileName.__class__.__name__ == 'str':
            self.getJavaClass().save(fileName, javaClass.valueOf(saveFormat))


class LoadOptions:

    @property
    def getLoadFormat(self):
        return self.__loadFormat

    @property
    def getJClass(self):
        return self.__jClass


class EpubLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.EPUB
    __jClass = jpype.JClass("com.aspose.python.pdf.EpubLoadOptions")


class HtmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.HTML
    __jClass = jpype.JClass("com.aspose.python.pdf.HtmlLoadOptions")


class MdLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MD
    __jClass = jpype.JClass("com.aspose.python.pdf.MdLoadOptions")


class MhtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MHT
    __jClass = jpype.JClass("com.aspose.python.pdf.MhtLoadOptions")


class PclLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PCL
    __jClass = jpype.JClass("com.aspose.python.pdf.PclLoadOptions")


class PdfXmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PDFXML
    __jClass = jpype.JClass("com.aspose.python.pdf.PdfXmlLoadOptions")


class PsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PS
    __jClass = jpype.JClass("com.aspose.python.pdf.PsLoadOptions")


class SvgLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.SVG
    __jClass = jpype.JClass("com.aspose.python.pdf.SvgLoadOptions")


class TeXLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TEX
    __jClass = jpype.JClass("com.aspose.python.pdf.TeXLoadOptions")


class TxtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TXT
    __jClass = jpype.JClass("com.aspose.python.pdf.TxtLoadOptions")


class XmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XML
    __jClass = jpype.JClass("com.aspose.python.pdf.XmlLoadOptions")


class XpsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XPS
    __jClass = jpype.JClass("com.aspose.python.pdf.XpsLoadOptions")


class XslFoLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XSLFO
    __jClass = jpype.JClass("com.aspose.python.pdf.XslFoLoadOptions")


class CgmLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.CGM
    __jClass = jpype.JClass("com.aspose.python.pdf.CgmLoadOptions")
