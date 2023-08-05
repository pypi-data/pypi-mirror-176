import jpype
import os

__asposepdf_dir__ = os.path.dirname(__file__)
__pdf_jar_path__ = __asposepdf_dir__ + "/jlib/aspose.pdf-python-22.7.1.jar"
jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % __pdf_jar_path__)
__all__ = ['Assist', 'Api']
